from app.infra.celery_app import celery_app
from app.services.openrouter_client import OpenRouterClient


@celery_app.task
def llm_request(prompt: str, user_id: int) -> str:
    client = OpenRouterClient()
    messages = [{"role": "user", "content": prompt}]
    answer = client.chat_completion_sync(messages)
    return answer
