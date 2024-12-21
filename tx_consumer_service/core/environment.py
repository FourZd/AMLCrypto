from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Core environment using pydantic settings."""
    RABBITMQ_QUEUE_NAME: str

    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int

    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_PORT: int
    POSTGRES_HOSTNAME: str
    DATABASE_DIALECT: str
    
    class Config:
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()


env = get_settings()
