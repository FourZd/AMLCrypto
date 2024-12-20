import pika
from schemas.dump_schemas import Transaction
from typing import List


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
        Publishes messages to a RabbitMQ queue in JSON format.

        :param transactions: List of transactions to publish
        :param queue_name: Name of the queue
        """
        if not self.channel:
            raise RuntimeError("No connection established. Call `connect` first.")

        # Declare the queue to ensure it exists
        self.channel.queue_declare(queue=queue_name)

        for transaction in transactions:
            # Serialize the transaction to JSON using Pydantic's json() method
            transaction_json = transaction.json()
            try:
                self.channel.basic_publish(exchange='', routing_key=queue_name, body=transaction_json)
            except Exception as e:
                print(e)
                print("Ошибка в паблише")
                
    def close_connection(self) -> None:
        """
        Закрывает соединение с RabbitMQ.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            self.channel = None