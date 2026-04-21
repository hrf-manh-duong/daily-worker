from fastapi.testclient import TestClient
from main import app


def test_timeline_has_events():
    client = TestClient(app)
    task = client.post("/tasks", json={"title": "Timeline task"}).json()
    client.post("/focus/start", json={"task_id": task["id"]})
    client.post("/focus/stop")
    client.post(f"/tasks/{task['id']}/complete")

    timeline = client.get("/timeline/today")
    assert timeline.status_code == 200
    assert len(timeline.json()) >= 4
