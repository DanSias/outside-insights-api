import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("user1@example.com", "password123", 201),
        ("invalid-email", "password123", 422),  # Invalid email format
    ],
)
def test_create_user(client: TestClient, email, password, status_code):
    """Test user registration."""
    response = client.post(
        "/api/v1/users/", json={"email": email, "password": password}
    )
    assert response.status_code == status_code


def test_login_user(client: TestClient):
    """Test user login with valid credentials."""
    client.post(
        "/api/v1/users/", json={"email": "test@example.com", "password": "password123"}
    )
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
