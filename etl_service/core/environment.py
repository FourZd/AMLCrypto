import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    INFURA_TOKEN: str
    DUMP_LINK: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str

    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int

    class Config:
        env_file = os.getenv("ENV_FILE")
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    settings = Settings()
    return settings


env = get_settings()
