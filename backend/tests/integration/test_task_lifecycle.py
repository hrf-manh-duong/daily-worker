from fastapi.testclient import TestClient
from main import app


def test_task_create_update_complete_flow():
    client = TestClient(app)
    created = client.post("/tasks", json={"title": "Write report"})
    assert created.status_code == 201
    task_id = created.json()["id"]

    updated = client.patch(f"/tasks/{task_id}", json={"title": "Write weekly report"})
    assert updated.status_code == 200
    assert updated.json()["title"] == "Write weekly report"

    completed = client.post(f"/tasks/{task_id}/complete")
    assert completed.status_code == 200
    assert completed.json()["status"] == "completed"
