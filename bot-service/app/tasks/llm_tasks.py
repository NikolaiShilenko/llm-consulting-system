import asyncio
from celery import Task
from app.infra.celery_app import celery_app
from app.services.openrouter_client import OpenRouterClient
from app.core.config import settings


class LLMTask(Task):
    _client = None

    @property
    def client(self):
        if self._client is None:
            self._client = OpenRouterClient()
        return self._client


@celery_app.task(base=LLMTask, bind=True)
async def llm_request(self, prompt: str, user_id: int) -> str:
    messages = [{"role": "user", "content": prompt}]
    answer = await self.client.chat_completion(messages)
    return answer
