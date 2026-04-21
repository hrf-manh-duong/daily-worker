from datetime import date, datetime, timedelta, timezone

from fastapi.testclient import TestClient

from api import dependencies
from main import app


def _fresh_client() -> TestClient:
    # Use a dedicated client. Standup tests should not assume isolation between tests,
    # because the app uses a module-level MemoryStore. Each test writes to unique dates.
    return TestClient(app)


def test_post_standup_happy_path():
    client = _fresh_client()
    payload = {
        "local_date": "2030-01-01",
        "yesterday": "- shipped feature A",
        "today": "review PRs",
        "blockers": "",
    }
    response = client.post("/standup", json=payload)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["local_date"] == "2030-01-01"
    assert body["today"] == "review PRs"
    assert body["blockers"] == ""
    assert "created_at" in body and "updated_at" in body


def test_post_standup_rejects_empty_today():
    client = _fresh_client()
    response = client.post(
        "/standup",
        json={"local_date": "2030-01-02", "yesterday": "", "today": "", "blockers": ""},
    )
    assert response.status_code == 422


def test_post_standup_rejects_oversized_field():
    client = _fresh_client()
    response = client.post(
        "/standup",
        json={
            "local_date": "2030-01-03",
            "yesterday": "x" * 4001,
            "today": "ok",
            "blockers": "",
        },
    )
    assert response.status_code == 422


def test_get_standup_404_for_missing():
    client = _fresh_client()
    response = client.get("/standup/2035-12-31")
    assert response.status_code == 404


def test_post_standup_overwrites_same_date():
    client = _fresh_client()
    local = "2030-02-01"
    first = client.post("/standup", json={"local_date": local, "today": "t1"}).json()
    second = client.post("/standup", json={"local_date": local, "today": "t2"}).json()
    assert first["created_at"] == second["created_at"]
    assert second["today"] == "t2"

    # list should contain only one entry for that date
    got = client.get(f"/standup/{local}").json()
    assert got["today"] == "t2"


def test_list_standups_newest_first_with_limit():
    client = _fresh_client()
    # Use year 2031 to avoid collisions with other tests in this module
    for day in (1, 3, 5):
        client.post(
            "/standup", json={"local_date": f"2031-03-0{day}", "today": f"day {day}"}
        )
    response = client.get("/standup?limit=2")
    assert response.status_code == 200
    entries = response.json()
    # filter to only the 2031-03 entries to avoid pollution
    march = [e for e in entries if e["local_date"].startswith("2031-03")]
    assert len(march) >= 2
    # The first two from our range should be the two newest
    dates = [e["local_date"] for e in entries[:2]]
    assert dates == sorted(dates, reverse=True)


def test_prefill_response_shape_and_header_parsing():
    client = _fresh_client()
    # Arrange: complete a task and backdate to 2032-06-14
    task = client.post("/tasks", json={"title": "Completed yesterday"}).json()
    client.post(f"/tasks/{task['id']}/complete")
    yesterday = date(2032, 6, 14)
    today = date(2032, 6, 15)
    dependencies.store.tasks[__import__("uuid").UUID(task["id"])].completed_at = (
        datetime.combine(yesterday, datetime.min.time(), tzinfo=timezone.utc)
        + timedelta(hours=10)
    )

    response = client.get("/standup/prefill", headers={"X-Client-Local-Date": today.isoformat()})
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["for_local_date"] == today.isoformat()
    assert body["source_local_date"] == yesterday.isoformat()
    assert "Completed yesterday" in body["completed_tasks"]
    assert body["prefill_markdown"].startswith("- ")


def test_prefill_invalid_header_returns_422():
    client = _fresh_client()
    response = client.get("/standup/prefill", headers={"X-Client-Local-Date": "not-a-date"})
    assert response.status_code == 422


def test_prefill_missing_header_falls_back_to_utc_today():
    client = _fresh_client()
    response = client.get("/standup/prefill")
    assert response.status_code == 200
    body = response.json()
    # Server fallback: for_local_date equals today (UTC)
    assert body["for_local_date"] == datetime.now(timezone.utc).date().isoformat()
