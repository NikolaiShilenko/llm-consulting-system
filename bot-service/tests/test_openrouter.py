import pytest
import respx
from httpx import Response
from app.services.openrouter_client import OpenRouterClient
from app.core.config import settings


@pytest.mark.asyncio
async def test_chat_completion_success():
    mock_response = {
        "choices": [{"message": {"content": "Hello from LLM"}}]
    }

    with respx.mock:
        respx.post(f"{settings.openrouter_base_url}/chat/completions").mock(
            Response(200, json=mock_response)
        )

        client = OpenRouterClient()
        result = await client.chat_completion([{"role": "user", "content": "Hi"}])

        assert result == "Hello from LLM"


@pytest.mark.asyncio
async def test_chat_completion_error():
    with respx.mock:
        respx.post(f"{settings.openrouter_base_url}/chat/completions").mock(
            Response(500, text="Internal Server Error")
        )

        client = OpenRouterClient()
        with pytest.raises(Exception, match="OpenRouter error 500"):
            await client.chat_completion([{"role": "user", "content": "Hi"}])
