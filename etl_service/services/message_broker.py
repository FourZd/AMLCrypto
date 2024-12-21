import pika
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

    def connect(self) -> None:
        """
        Устанавливает соединение с RabbitMQ.
        """
        credentials = pika.PlainCredentials(self.user, self.password)
        connection_params = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(connection_params)
        self.channel = self.connection.channel()

    def publish_to_queue(self, transactions: List['Transaction'], queue_name: str) -> None:
        """
        Publishes a batch of transactions to a RabbitMQ queue in JSON format.

        :param transactions: List of transactions to publish
        :param queue_name: Name of the queue
        """
        if not self.channel:
            raise RuntimeError("No connection established. Call `connect` first.")

        logger.info("Declaring transaction queue")
        self.channel.queue_declare(queue=queue_name, durable=True)

        logger.info("Serializing transactions to JSON")
        try:
            # Сериализуем список транзакций в JSON
            transactions_json = json.dumps([json.loads(transaction.json()) for transaction in transactions])
            logger.info("Publishing transactions batch to MQ")
            self.channel.basic_publish(exchange='', routing_key=queue_name, body=transactions_json)
            logger.info("Batch published successfully!")
        except Exception as e:
            logger.error(f"Failed to publish transactions batch: {e}")
                
    def close_connection(self) -> None:
        """
        Закрывает соединение с RabbitMQ.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            self.channel = None