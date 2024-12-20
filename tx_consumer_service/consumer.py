import asyncio
import aio_pika
import json
from core.logger import logger
from schemas import Transaction as TransactionSchema
from services import TransactionService


class Consumer:
    def __init__(self, rabbitmq_url: str, queue_name: str, transaction_service: TransactionService):
        """
        Initialize the RabbitMQ consumer.

        :param rabbitmq_url: Connection URL for RabbitMQ
        :param queue_name: Name of the queue to listen to
        :param transaction_service: Service to handle transaction-related operations
        """
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.transaction_service = transaction_service

    async def process_message(self, message: aio_pika.IncomingMessage):
        """
        Process a single message from the RabbitMQ queue.

        :param message: The incoming message from RabbitMQ
        """
        async with message.process():
            try:
                transactions_data = json.loads(message.body)
                transactions = [TransactionSchema(**data) for data in transactions_data]

                transaction_hashes = [txn.hash for txn in transactions]
                existing_hashes = await self.transaction_service.get_existing_transaction_hashes(transaction_hashes)
                new_transactions = [txn for txn in transactions if txn.hash not in existing_hashes]

                if new_transactions:
                    await self.transaction_service.add(new_transactions)
                    logger.info(f"Successfully saved {len(new_transactions)} new transactions.")
                else:
                    logger.info("No new transactions to save.")
            except Exception as e:
                logger.error(f"Error processing message: {e}")

    async def start_consuming(self):
        """
        Start consuming messages from the RabbitMQ queue.
        """
        connection = await aio_pika.connect_robust(self.rabbitmq_url)

        async with connection:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=1)

            queue = await channel.declare_queue(self.queue_name, durable=True)
            logger.info(f"Listening to RabbitMQ queue: {self.queue_name}")

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    await self.process_message(message)