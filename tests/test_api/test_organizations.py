import pytest
from fastapi.testclient import TestClient


def test_create_organization(client: TestClient):
    """Test organization creation."""
    response = client.post("/api/v1/organizations/", json={"name": "Test Org"})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Org"


def test_get_organization(client: TestClient):
    """Test retrieving organization details."""
    response = client.get("/api/v1/organizations/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
