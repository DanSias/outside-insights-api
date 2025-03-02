import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.orm import Session

from app.services.llm_service import LLMService
from app.models.llm_provider import LLMProvider
from app.models.prompt import Prompt


@pytest.fixture
def mock_db():
    """Fixture to mock the database session."""
    return MagicMock(spec=Session)


@pytest.fixture
def mock_prompt():
    """Fixture to mock a Prompt object."""
    prompt = MagicMock(spec=Prompt)
    prompt.id = 1
    prompt.content = "Test prompt content"
    return prompt


@pytest.fixture
def mock_provider():
    """Fixture to mock an LLMProvider object."""
    provider = MagicMock(spec=LLMProvider)
    provider.id = 1
    provider.name = "openai"
    provider.api_base_url = "https://api.openai.com/v1"
    provider.config = {"api_key": "test_key"}
    return provider


@pytest.mark.asyncio
async def test_process_prompt(mock_db, mock_prompt, mock_provider):
    """Test that process_prompt correctly interacts with the LLM provider and stores the response."""
    # Setup
    llm_service = LLMService()

    with patch(
        "app.db.crud.llm_provider.get_provider_by_name", return_value=mock_provider
    ):
        llm_service._send_to_provider = AsyncMock(
            return_value=("Test response", {"token_count": 10})
        )

        with patch("app.db.crud.response.create_response") as mock_create_response:
            mock_response = MagicMock()
            mock_create_response.return_value = mock_response

            # Act
            result = await llm_service.process_prompt(mock_db, mock_prompt, "openai")

            # Assert
            assert result == mock_response
            llm_service._send_to_provider.assert_called_once_with(
                "openai", mock_prompt.content, None
            )
            mock_create_response.assert_called_once()

            # Check response parameters
            _, kwargs = mock_create_response.call_args
            assert kwargs["prompt_id"] == mock_prompt.id
            assert kwargs["llm_provider_id"] == mock_provider.id
            assert kwargs["content"] == "Test response"
            assert kwargs["token_count"] == 10
            assert "latency" in kwargs


@pytest.mark.asyncio
async def test_process_openai(mock_provider):
    """Test that OpenAI API request returns expected values."""
    llm_service = LLMService()

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Test response"}}],
        "model": "gpt-4",
        "usage": {"total_tokens": 10, "prompt_tokens": 5, "completion_tokens": 5},
    }

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post.return_value = (
            mock_response
        )

        # Act
        content, metadata = await llm_service._call_openai(
            mock_provider, "Test prompt", {"model": "gpt-4"}
        )

        # Assert
        assert content == "Test response"
        assert metadata == {
            "model": "gpt-4",
            "token_count": 10,
            "prompt_tokens": 5,
            "completion_tokens": 5,
        }
