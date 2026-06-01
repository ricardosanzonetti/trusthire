from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_candidates_endpoint():
    response = client.get("/candidates/")
    assert response.status_code == 200
