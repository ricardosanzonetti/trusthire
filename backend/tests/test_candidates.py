from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def unique_email(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}@test.com"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200


def test_get_candidates():
    response = client.get("/candidates/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_candidate_by_id():
    email = unique_email("getbyid")

    create_response = client.post(
        "/candidates/",
        json={
            "full_name": "Get By ID User",
            "email": email,
            "linkedin_url": "https://linkedin.com/in/getbyid"
        }
    )

    candidate_id = create_response.json()["id"]

    response = client.get(
        f"/candidates/{candidate_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == candidate_id
    assert data["email"] == email


def test_update_candidate():
    email = unique_email("update")

    create_response = client.post(
        "/candidates/",
        json={
            "full_name": "Old Name",
            "email": email,
            "linkedin_url": "https://linkedin.com/in/old"
        }
    )

    candidate_id = create_response.json()["id"]

    response = client.put(
        f"/candidates/{candidate_id}",
        json={
            "full_name": "New Name",
            "email": email,
            "linkedin_url": "https://linkedin.com/in/new"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["full_name"] == "New Name"
    assert data["linkedin_url"] == "https://linkedin.com/in/new"


def test_delete_candidate():
    email = unique_email("delete")

    create_response = client.post(
        "/candidates/",
        json={
            "full_name": "Delete Test",
            "email": email,
            "linkedin_url": "https://linkedin.com/in/delete"
        }
    )

    candidate_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/candidates/{candidate_id}"
    )

    assert delete_response.status_code == 200

    get_response = client.get(
        f"/candidates/{candidate_id}"
    )

    assert get_response.status_code == 404


def test_verify_linkedin():
    email = unique_email("verify")

    create_response = client.post(
        "/candidates/",
        json={
            "full_name": "Verify Test",
            "email": email,
            "linkedin_url": "https://linkedin.com/in/verify"
        }
    )

    candidate_id = create_response.json()["id"]

    response = client.post(
        f"/candidates/{candidate_id}/verify-linkedin"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["verification_status"] == "verified"


def test_duplicate_email():
    email = unique_email("duplicate")

    response_1 = client.post(
        "/candidates/",
        json={
            "full_name": "First User",
            "email": email,
            "linkedin_url": "https://linkedin.com/in/first"
        }
    )

    assert response_1.status_code == 200

    response_2 = client.post(
        "/candidates/",
        json={
            "full_name": "Second User",
            "email": email,
            "linkedin_url": "https://linkedin.com/in/second"
        }
    )

    assert response_2.status_code == 409

    assert response_2.json() == {
        "detail": "Email already exists"
    }