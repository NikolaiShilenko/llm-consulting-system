import httpx
from app.core.config import settings


class OpenRouterClient:
    def __init__(self):
        self.base_url = settings.openrouter_base_url
        self.api_key = settings.openrouter_api_key
        self.model = settings.openrouter_model

    async def chat_completion(self, messages: list[dict[str, str]], temperature: float = 0.7) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code != 200:
                raise Exception(f"OpenRouter error {response.status_code}: {response.text}")
            data = response.json()
            return data["choices"][0]["message"]["content"]

    def chat_completion_sync(self, messages: list[dict[str, str]], temperature: float = 0.7) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        with httpx.Client(timeout=120.0) as client:
            response = client.post(url, headers=headers, json=payload)
            if response.status_code != 200:
                raise Exception(f"OpenRouter error {response.status_code}: {response.text}")
            data = response.json()
            return data["choices"][0]["message"]["content"]
