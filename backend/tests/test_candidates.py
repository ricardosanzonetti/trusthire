from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200


def test_get_candidates_endpoint():
    response = client.get("/candidates/")
    assert response.status_code == 200


def test_get_candidate_not_found():
    response = client.get("/candidates/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Candidate not found"
    }

def test_create_candidate():
    response = client.post(
        "/candidates/",
        json={
            "full_name": "Test User Pytest",
            "email": "pytest_user_001@test.com",
            "linkedin_url": "https://linkedin.com/in/pytest-user"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["full_name"] == "Test User Pytest"
    assert data["email"] == "pytest_user_001@test.com"