import requests
import pandas as pd
import pika
from services.dumper import Dumper
from services.message_broker import MessageBroker
from services.transaction_observer import TransactionObserver
import asyncio
from core.environment import env


async def main():
    print("Entering main")

    # Использовал дамп транзакций Ethereum за 30 июля 2015 года, т.к. он небольшой и быстро загружается.
    # При необходимости могу сделать также чтобы оно парсило все дампы с blockchair, храня информацию о последней запаршенной дате.
    # однако тестирование подобной штуки очень затруднилось бы тем, что блокчейр выдает 402 ошибку без VPNа, а с впном скачать даже 50 мб крайне долго(
    DUMP_URL = env.DUMP_LINK

    # Загружаем и обрабатываем дамп файл.
    dumper = Dumper(DUMP_URL, "dumps")
    await dumper.download()
    dump_transactions = dumper.process()
    print(dump_transactions)

    # Подключаемся к RabbitMQ
    queue_name = "ethereum_transactions"
    message_broker = MessageBroker()
    message_broker.connect()
    message_broker.publish_to_queue(queue_name, dump_transactions)

    # Подключаемся к ноде Ethereum
    provider_url = f"wss://mainnet.infura.io/ws/v3/{env.INFURA_TOKEN}"
    observer = TransactionObserver(provider_url, message_broker)
    await observer.observe()


if __name__ == "__main__":
    asyncio.run(main())
