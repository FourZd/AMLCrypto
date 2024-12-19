import requests
import pandas as pd
import pika
from services.dumper import Dumper
from services.message_broker import MessageBroker
from services.transaction_observer import TransactionObserver
import asyncio


async def main():
    print("Entering main")

    # Используется дамп транзакций Ethereum за 30 июля 2015 года, т.к. он небольшой и быстро обрабатывается
    url = "https://gz.blockchair.com/ethereum/transactions/blockchair_ethereum_transactions_20150730.tsv.gz"

    dumper = Dumper(url, 'dumps')
    await dumper.download()
    dump_transactions = dumper.process()
    print(dump_transactions)

    # Подключаемся к RabbitMQ
    queue_name = 'ethereum_transactions'
    message_broker = MessageBroker()
    message_broker.connect()
    message_broker.publish_to_queue(queue_name, transaction_dump)

    # Подключаемся к ноде Ethereum
    provider_url = "wss://mainnet.infura.io/ws/v3/your_infura_project_id"
    observer = TransactionObserver(provider_url, message_broker)
    await observer.observe()
    



if __name__ == "__main__":
    asyncio.run(main())
