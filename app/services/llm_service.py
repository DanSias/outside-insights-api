import time
import httpx
import logging
from typing import Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session

from app.config import (
    OPENAI_API_KEY,
    OPENAI_API_BASE_URL,
    ANTHROPIC_API_KEY,
    ANTHROPIC_API_BASE_URL,
    COHERE_API_KEY,
    COHERE_API_BASE_URL,
    GEMINI_API_KEY,
    GEMINI_API_BASE_URL,
    DEEPSEEK_API_KEY,
    DEEPSEEK_API_BASE_URL,
)
from app.models.llm_provider import LLMProvider
from app.models.prompt import Prompt
from app.models.response import Response
from app.db.crud.llm_provider import get_provider_by_name
from app.db.crud.response import create_response

logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with LLM providers"""

    async def process_prompt(
        self,
        db: Session,
        prompt: Prompt,
        provider_name: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Response:
        """
        Process a prompt using the specified LLM provider.

        Args:
            db: Database session
            prompt: The prompt to process
            provider_name: Name of the LLM provider to use
            parameters: Optional parameters for the LLM request

        Returns:
            Response object containing the LLM's response
        """
        provider = get_provider_by_name(db, name=provider_name)
        if not provider:
            raise ValueError(f"LLM provider '{provider_name}' not found")

        start_time = time.time()
        response_content, metadata = await self._send_to_provider(
            provider_name.lower(), prompt.content, parameters
        )
        latency = time.time() - start_time

        response = create_response(
            db=db,
            prompt_id=prompt.id,
            llm_provider_id=provider.id,
            content=response_content,
            metadata=metadata,
            latency=latency,
            token_count=metadata.get("token_count", 0),
        )

        return response

    async def _send_to_provider(
        self,
        provider_name: str,
        prompt_content: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Send a prompt to the specified LLM provider.

        Args:
            provider_name: Name of the provider (e.g., "openai", "gemini")
            prompt_content: Content of the prompt
            parameters: Optional parameters for the request

        Returns:
            Tuple of (response_content, metadata)
        """
        if parameters is None:
            parameters = {}

        provider_methods = {
            "openai": self._call_openai,
            "anthropic": self._call_anthropic,
            "cohere": self._call_cohere,
            "gemini": self._call_gemini,
            "deepseek": self._call_deepseek,
        }

        if provider_name in provider_methods:
            return await provider_methods[provider_name](prompt_content, parameters)

        raise ValueError(f"Unsupported LLM provider: {provider_name}")

    async def _make_api_request(
        self,
        url: str,
        headers: Dict[str, str],
        payload: Dict[str, Any],
        method: str = "POST",
    ) -> Dict[str, Any]:
        """Handles HTTP API requests with error handling."""
        async with httpx.AsyncClient() as client:
            try:
                if method == "POST":
                    response = await client.post(url, json=payload, headers=headers)
                else:
                    response = await client.get(url, params=payload, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"API request error: {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                raise

    # ------------------ OpenAI ------------------ #
    async def _call_openai(
        self, prompt_content: str, parameters: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        url = f"{OPENAI_API_BASE_URL}/chat/completions"
        payload = {
            "model": parameters.get("model", "gpt-4o"),
            "messages": [{"role": "user", "content": prompt_content}],
            "temperature": parameters.get("temperature", 0.7),
            "max_tokens": parameters.get("max_tokens", 500),
        }
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        result = await self._make_api_request(url, headers, payload)

        return result["choices"][0]["message"]["content"], {
            "model": result["model"],
            "token_count": result["usage"]["total_tokens"],
        }

    # ------------------ Anthropic ------------------ #
    async def _call_anthropic(
        self, prompt_content: str, parameters: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        url = f"{ANTHROPIC_API_BASE_URL}/v1/messages"
        payload = {
            "model": parameters.get("model", "claude-3-opus-20240229"),
            "messages": [{"role": "user", "content": prompt_content}],
            "temperature": parameters.get("temperature", 0.7),
            "max_tokens": parameters.get("max_tokens", 500),
        }
        headers = {"x-api-key": ANTHROPIC_API_KEY, "Content-Type": "application/json"}
        result = await self._make_api_request(url, headers, payload)

        return result["content"][0]["text"], {
            "model": result["model"],
            "token_count": result.get("usage", {}).get("input_tokens", 0),
        }

    # ------------------ Cohere ------------------ #
    async def _call_cohere(
        self, prompt_content: str, parameters: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        url = f"{COHERE_API_BASE_URL}/v1/generate"
        payload = {
            "model": parameters.get("model", "command"),
            "prompt": prompt_content,
            "temperature": parameters.get("temperature", 0.7),
        }
        headers = {
            "Authorization": f"Bearer {COHERE_API_KEY}",
            "Content-Type": "application/json",
        }
        result = await self._make_api_request(url, headers, payload)

        return result["generations"][0]["text"], {
            "model": result.get("model", ""),
            "token_count": sum(result.get("meta", {}).get("billed_units", {}).values()),
        }

    # ------------------ Gemini ------------------ #
    async def _call_gemini(
        self, prompt_content: str, parameters: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        url = f"{GEMINI_API_BASE_URL}/text/generate"
        payload = {
            "model": parameters.get("model", "gemini-pro"),
            "prompt": prompt_content,
            "temperature": parameters.get("temperature", 0.7),
        }
        headers = {
            "Authorization": f"Bearer {GEMINI_API_KEY}",
            "Content-Type": "application/json",
        }
        result = await self._make_api_request(url, headers, payload)

        return result["candidates"][0]["content"], {
            "model": result["model"],
            "token_count": result.get("usage", {}).get("total_tokens", 0),
        }

    # ------------------ DeepSeek ------------------ #
    async def _call_deepseek(
        self, prompt_content: str, parameters: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        url = f"{DEEPSEEK_API_BASE_URL}/generate"
        payload = {
            "prompt": prompt_content,
            "temperature": parameters.get("temperature", 0.7),
        }
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        }
        result = await self._make_api_request(url, headers, payload)

        return result["response"], {
            "model": result.get("model", ""),
            "token_count": result.get("usage", {}).get("total_tokens", 0),
        }


# Create a singleton instance
llm_service = LLMService()
