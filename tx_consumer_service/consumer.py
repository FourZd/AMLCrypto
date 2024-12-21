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

        Args:
            rabbitmq_url (str): Connection URL for RabbitMQ.
            queue_name (str): Queue name to consume from.
            transaction_service (TransactionService): Transaction service for handling data.
        """
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.transaction_service = transaction_service

    async def process_message(self, message: aio_pika.IncomingMessage):
        """
        Process a single message from RabbitMQ.

        Args:
            message (aio_pika.IncomingMessage): Incoming RabbitMQ message.
        """
        async with message.process():
            logger.info("Processing message")
            try:
                transactions_data = json.loads(message.body)
                transactions = [TransactionSchema(**data) for data in transactions_data]
                logger.info(f"Received {len(transactions)} transactions")
                transaction_hashes = [txn.hash for txn in transactions]
                logger.info("Checking for existing transactions")
                existing_hashes = await self.transaction_service.get_existing_transaction_hashes(transaction_hashes)
                logger.info(f"Found {len(existing_hashes)} existing transactions")
                new_transactions = [txn for txn in transactions if txn.hash not in existing_hashes]
                
                if new_transactions:
                    logger.info(f"Saving {len(new_transactions)} new transactions")
                    await self.transaction_service.add(new_transactions)
                    logger.info(f"Successfully saved {len(new_transactions)} new transactions.")
                else:
                    logger.info("No new transactions to save.")
            except Exception as e:
                logger.error(f"Error processing message: {e}")

    async def start_consuming(self):
        """
        Start consuming messages from RabbitMQ.
        """
        connection = await aio_pika.connect_robust(self.rabbitmq_url)
        logger.info("Connected to RabbitMQ")
        async with connection:
            channel = await connection.channel()
            logger.info("Channel created")
            await channel.set_qos(prefetch_count=1)
            logger.info("QoS set")
            queue = await channel.declare_queue(self.queue_name, durable=True)
            logger.info(f"Listening to RabbitMQ queue: {self.queue_name}")

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    logger.info("Message received")
                    await self.process_message(message)