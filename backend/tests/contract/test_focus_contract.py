from fastapi.testclient import TestClient
from main import app


def test_focus_contract_conflict():
    client = TestClient(app)
    task = client.post("/tasks", json={"title": "Focus"}).json()
    assert client.post("/focus/start", json={"task_id": task["id"]}).status_code == 201
    assert client.post("/focus/start", json={"task_id": task["id"]}).status_code == 409
