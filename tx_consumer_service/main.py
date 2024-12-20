from core.environment import env
from repositories import repository_factory
from core.database import database_factory
from services import service_factory
from core.logger import logger
from consumer import Consumer
import asyncio


async def main():
    RABBITMQ_URL = f"amqp://{env.RABBITMQ_DEFAULT_USER}:{env.RABBITMQ_DEFAULT_PASS}@{env.RABBITMQ_HOST}:{env.RABBITMQ_PORT}/"

    db = database_factory(
        f"{env.DATABASE_DIALECT}+asyncpg://{env.POSTGRES_USER}:{env.POSTGRES_PASSWORD}@{env.POSTGRES_HOSTNAME}:{env.POSTGRES_PORT}/{env.POSTGRES_DB}"
    )
    tx_service = service_factory(
        repository_factory(db.session)
    )

    consumer = Consumer(
        rabbitmq_url=RABBITMQ_URL, 
        queue_name=env.RABBITMQ_QUEUE_NAME, 
        transaction_service=tx_service
    )

    try:
        await consumer.start_consuming()
    except Exception as e:
        logger.error(f"Error during consumption: {e}")

if __name__ == "__main__":
    asyncio.run(main())
