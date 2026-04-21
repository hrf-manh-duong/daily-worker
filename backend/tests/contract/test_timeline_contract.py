from fastapi.testclient import TestClient
from main import app


def test_timeline_contract():
    client = TestClient(app)
    response = client.get("/timeline/today")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
