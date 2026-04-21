from fastapi.testclient import TestClient
from main import app
from api.dependencies import store


def test_single_active_focus():
    store.tasks.clear()
    store.focus_sessions.clear()
    store.events.clear()
    client = TestClient(app)
    task = client.post("/tasks", json={"title": "Focus task"}).json()
    start = client.post("/focus/start", json={"task_id": task["id"]})
    assert start.status_code == 201

    second_start = client.post("/focus/start", json={"task_id": task["id"]})
    assert second_start.status_code == 409

    stop = client.post("/focus/stop")
    assert stop.status_code == 200
