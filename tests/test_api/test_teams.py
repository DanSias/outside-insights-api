import pytest
from fastapi.testclient import TestClient


def test_create_team(client: TestClient):
    """Test creating a new team."""
    response = client.post(
        "/api/v1/teams/", json={"name": "Dev Team", "organization_id": 1}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Dev Team"


def test_get_teams(client: TestClient):
    """Test retrieving teams list."""
    response = client.get("/api/v1/teams/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
