from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = Field(default="bot-service", alias="APP_NAME")
    env: str = Field(default="local", alias="ENV")

    telegram_bot_token: str = Field(alias="TELEGRAM_BOT_TOKEN")

    jwt_secret: str = Field(alias="JWT_SECRET")
    jwt_alg: str = Field(default="HS256", alias="JWT_ALG")

    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    rabbitmq_url: str = Field(default="amqp://guest:guest@localhost:5672/", alias="RABBITMQ_URL")

    openrouter_api_key: str = Field(alias="OPENROUTER_API_KEY")
    openrouter_base_url: str = Field(default="https://openrouter.ai/api/v1", alias="OPENROUTER_BASE_URL")
    openrouter_model: str = Field(default="openai/gpt-3.5-turbo", alias="OPENROUTER_MODEL")
    openrouter_site_url: str = Field(default="https://example.com", alias="OPENROUTER_SITE_URL")
    openrouter_app_name: str = Field(default="bot-service", alias="OPENROUTER_APP_NAME")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
