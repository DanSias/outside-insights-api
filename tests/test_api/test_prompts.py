import pytest
from fastapi.testclient import TestClient


def test_submit_prompt(client: TestClient):
    """Test submitting a new prompt."""
    response = client.post(
        "/api/v1/prompts/", json={"content": "What is AI?", "llm_provider": "openai"}
    )
    assert response.status_code == 201
    assert "prompt_id" in response.json()


def test_get_prompt(client: TestClient):
    """Test retrieving a specific prompt."""
    response = client.get("/api/v1/prompts/1")
    assert response.status_code == 200
    assert response.json()["prompt_id"] == "1"
