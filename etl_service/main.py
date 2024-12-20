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
    print("Downloading dump")
    # Загружаем и обрабатываем дамп файл.
    dumper = Dumper(DUMP_URL, "dumps")
    await dumper.download()
    print("Dump downloaded")
    dump_transactions = dumper.process()
    print("Processing dump")
    # Подключаемся к RabbitMQ
    queue_name = "ethereum_transactions"
    print(queue_name)
    message_broker = MessageBroker(
        user=env.RABBITMQ_DEFAULT_USER,
        password=env.RABBITMQ_DEFAULT_PASS,
        host=env.RABBITMQ_HOST,
        port=env.RABBITMQ_PORT
    )
    print("Initialized message broker")
    message_broker.connect()
    print("Connected to message broker")
    try:
        message_broker.publish_to_queue(dump_transactions, queue_name)
        print("Published dump to the queue")
    except Exception as e:
        error_message = str(e)
        print("Ошибка:", error_message[:500])
    # Подключаемся к ноде Ethereum
    print(env.INFURA_TOKEN)
    provider_url = f"wss://mainnet.infura.io/ws/v3/{env.INFURA_TOKEN}"
    print("provider url defined")
    observer = TransactionObserver(message_broker)
    print("Initialized observer")
    await observer.observe(provider_url)
    print("Observed")


if __name__ == "__main__":
    asyncio.run(main())
