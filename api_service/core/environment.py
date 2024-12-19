import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_PORT: int
    POSTGRES_HOSTNAME: str
    DATABASE_DIALECT: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: str
    REDIS_PASSWORD: str

    class Config:
        env_file = os.getenv("ENV_FILE")
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    """Функция для получения настроек в зависимости от среды."""
    settings = Settings()
    return settings


env = get_settings()
