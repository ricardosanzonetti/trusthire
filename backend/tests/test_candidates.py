from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def unique_email(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}@test.com"


def get_auth_headers():
    email = unique_email("user")

    client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "123456"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "123456"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200


def test_get_candidates():
    headers = get_auth_headers()

    response = client.get(
        "/candidates/",
        headers=headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_candidate_by_id():
    headers = get_auth_headers()

    email = unique_email("getbyid")

    create_response = client.post(
        "/candidates/",
        headers=headers,
        json={
            "full_name": "Get By ID User",
            "email": email,
            "linkedin_url": "https://linkedin.com/in/getbyid"
        }
    )

    candidate_id = create_response.json()["id"]

    response = client.get(
        f"/candidates/{candidate_id}",
        headers=headers
    )

    assert response.status_code == 200


def test_update_candidate():
    headers = get_auth_headers()

    email = unique_email("update")

    create_response = client.post(
        "/candidates/",
        headers=headers,
        json={
            "full_name": "Old Name",
            "email": email,
            "linkedin_url": "https://linkedin.com/in/old"
        }
    )

    candidate_id = create_response.json()["id"]

    response = client.put(
        f"/candidates/{candidate_id}",
        headers=headers,
        json={
            "full_name": "New Name",
            "email": email,
            "linkedin_url": "https://linkedin.com/in/new"
        }
    )

    assert response.status_code == 200


def test_delete_candidate():
    headers = get_auth_headers()

    email = unique_email("delete")

    create_response = client.post(
        "/candidates/",
        headers=headers,
        json={
            "full_name": "Delete Test",
            "email": email,
            "linkedin_url": "https://linkedin.com/in/delete"
        }
    )

    candidate_id = create_response.json()["id"]

    response = client.delete(
        f"/candidates/{candidate_id}",
        headers=headers
    )

    assert response.status_code == 200


def test_verify_linkedin():
    headers = get_auth_headers()

    email = unique_email("verify")

    create_response = client.post(
        "/candidates/",
        headers=headers,
        json={
            "full_name": "Verify Test",
            "email": email,
            "linkedin_url": "https://linkedin.com/in/verify"
        }
    )

    candidate_id = create_response.json()["id"]

    response = client.post(
        f"/candidates/{candidate_id}/verify-linkedin",
        headers=headers
    )

    assert response.status_code == 200


def test_duplicate_email():
    headers = get_auth_headers()

    email = unique_email("duplicate")

    response_1 = client.post(
        "/candidates/",
        headers=headers,
        json={
            "full_name": "First User",
            "email": email,
            "linkedin_url": "https://linkedin.com/in/first"
        }
    )

    assert response_1.status_code == 200

    response_2 = client.post(
        "/candidates/",
        headers=headers,
        json={
            "full_name": "Second User",
            "email": email,
            "linkedin_url": "https://linkedin.com/in/second"
        }
    )

    assert response_2.status_code == 409


def test_get_candidate_not_found():
    headers = get_auth_headers()

    response = client.get(
        "/candidates/999999",
        headers=headers
    )

    assert response.status_code == 404


def test_update_candidate_not_found():
    headers = get_auth_headers()

    response = client.put(
        "/candidates/999999",
        headers=headers,
        json={
            "full_name": "Nobody",
            "email": "nobody@test.com",
            "linkedin_url": "https://linkedin.com/in/nobody"
        }
    )

    assert response.status_code == 404


def test_delete_candidate_not_found():
    headers = get_auth_headers()

    response = client.delete(
        "/candidates/999999",
        headers=headers
    )

    assert response.status_code == 404


def test_verify_linkedin_not_found():
    headers = get_auth_headers()

    response = client.post(
        "/candidates/999999/verify-linkedin",
        headers=headers
    )

    assert response.status_code == 404