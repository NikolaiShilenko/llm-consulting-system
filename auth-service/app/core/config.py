from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = Field(default="auth-service", alias="APP_NAME")
    env: str = Field(default="local", alias="ENV")

    jwt_secret: str = Field(alias="JWT_SECRET")
    jwt_alg: str = Field(default="HS256", alias="JWT_ALG")
    access_token_expire_minutes: int = Field(default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    sqlite_path: str = Field(default="./auth.db", alias="SQLITE_PATH")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
