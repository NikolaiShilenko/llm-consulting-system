FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    fastapi uvicorn aiogram celery redis httpx pydantic-settings python-jose[cryptography] ruff aiohttp-socks

COPY . .

ENV PYTHONPATH=/app

CMD ["celery", "-A", "app.infra.celery_app", "worker", "--loglevel=info"]