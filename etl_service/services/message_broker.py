import aio_pika
from schemas.transaction_schemas import Transaction
from typing import List
from core.logger import logger
import json


class MessageBroker:
    def __init__(self, user: str, password: str, host: str, port: int):
        """
        Инициализация брокера сообщений с заданными параметрами.

        :param user: Имя пользователя для подключения к RabbitMQ
        :param password: Пароль пользователя
        :param host: Хост RabbitMQ
        :param port: Порт RabbitMQ
        """
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self.connection = None
        self.channel = None

    async def connect(self) -> None:
        """
        Connects to RabbitMQ using the provided credentials.
        """
        logger.info("Connecting to RabbitMQ")
        self.connection = await aio_pika.connect_robust(
            f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"
        )
        self.channel = await self.connection.channel()

    async def publish_to_queue(self, transactions: List['Transaction'], queue_name: str) -> None:
        """
        Publishes a batch of transactions to a RabbitMQ queue in JSON format.

        :param transactions: List of transactions to publish
        :param queue_name: Name of the queue
        """
        if not self.channel:
            raise RuntimeError("No connection established. Call `connect` first.")

        logger.info("Declaring transaction queue")
        await self.channel.declare_queue(queue_name, durable=True)

        logger.info("Serializing transactions to JSON")
        try:
            transactions_json = json.dumps([json.loads(transaction.json()) for transaction in transactions])
            logger.info("Publishing transactions batch to MQ")

            await self.channel.default_exchange.publish(
                aio_pika.Message(body=transactions_json.encode('utf-8')),
                routing_key=queue_name
            )

            logger.info("Batch published successfully!")
        except Exception as e:
            logger.error(f"Failed to publish transactions batch: {e}")