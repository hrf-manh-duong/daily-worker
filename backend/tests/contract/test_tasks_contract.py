from fastapi.testclient import TestClient
from main import app


def test_tasks_contract_basic():
    client = TestClient(app)
    response = client.post("/tasks", json={"title": "Contract Task"})
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert body["status"] in {"active", "completed"}
