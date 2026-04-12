FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    fastapi uvicorn aiogram celery redis httpx pydantic-settings python-jose[cryptography] ruff aiohttp-socks

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]