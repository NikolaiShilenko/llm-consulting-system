FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    fastapi uvicorn sqlalchemy aiosqlite pydantic pydantic-settings \
    python-jose[cryptography] ruff greenlet \
    python-multipart email-validator \
    bcrypt==4.0.1 \
    passlib==1.7.4

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]