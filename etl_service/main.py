from services.dumper import Dumper
from services.message_broker import MessageBroker
from services.transaction_observer import TransactionObserver
import asyncio
from core.environment import env
from core.logger import logger
from core.redis_client import RedisPool


async def main():
    redis_pool = RedisPool(f"redis://:{env.REDIS_PASSWORD}@{env.REDIS_HOST}:{env.REDIS_PORT}/{env.REDIS_DB}")

    dumper = Dumper(env.DUMP_LINK, "dumps", redis_pool)
    logger.info("Starting the ETL process")
    last_processed_date = await dumper.get_last_processed_date()
    logger.info(f"Last processed date: {last_processed_date}")
    if last_processed_date:
        current_date = dumper.get_next_date(last_processed_date)
    else:
        current_date = env.DUMP_LINK.split("_")[-1].split(".")[0]
    logger.info(f"Starting from date {current_date}")

    queue_name = "ethereum_transactions"
    message_broker = MessageBroker(
        user=env.RABBITMQ_DEFAULT_USER,
        password=env.RABBITMQ_DEFAULT_PASS,
        host=env.RABBITMQ_HOST,
        port=env.RABBITMQ_PORT
    )
    logger.info("Connecting to the message broker")
    await message_broker.connect()
    logger.info("Connected to the message broker!")
    for _ in range(2):
        dump_url = f"https://gz.blockchair.com/ethereum/transactions/blockchair_ethereum_transactions_{current_date}.tsv.gz"
        try:
            dumper.dump_url = dump_url
            logger.info(f"Downloading dump for date {current_date}")
            await dumper.download()
            logger.info("Dump downloaded! Processing...")
            dump_transactions = dumper.process()
            logger.info("Dump processed! Now publishing to the queue...")
            await message_broker.publish_to_queue(dump_transactions, queue_name)
            logger.info("Successfully published to the queue! Setting last processed date...")
            await dumper.set_last_processed_date(current_date)
            current_date = dumper.get_next_date(current_date)
            logger.info(f"Next current date is {current_date}")
        except Exception as e:
            logger.error(f"Failed to process dump for date {current_date}: {e}")
            break

        if _ == 1:
            logger.info("FOR DEVELOPING REASONS, IT WONT DOWNLOAD EVERY DUMP, ONLY THE FIRST TWO")
            break

    logger.info("Woah, finished processing dumps, starting the observer now!")
    provider_url = f"wss://mainnet.infura.io/ws/v3/{env.INFURA_TOKEN}"
    observer = TransactionObserver(message_broker)
    logger.info("Observing...")
    await observer.observe(provider_url, queue_name)
    

if __name__ == "__main__":
    asyncio.run(main())
