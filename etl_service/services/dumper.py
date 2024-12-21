import aiohttp
import os
from urllib.parse import urlparse
import pandas as pd
from typing import List
from schemas.transaction_schemas import Transaction
from core.redis_client import RedisPool
from datetime import datetime, timedelta
from core.logger import logger


class Dumper:

    def __init__(self, dump_url: str, output_dir: str, redis_pool: RedisPool):
        self.dump_url = dump_url
        self.output_dir = output_dir
        self.redis_pool = redis_pool

        self.file_name = os.path.basename(urlparse(self.dump_url).path)
        self.output_file = os.path.join(self.output_dir, self.file_name)

        os.makedirs(self.output_dir, exist_ok=True)

    async def download(self) -> None:
        """Downloads the dump file from the provided URL"""
        async with aiohttp.ClientSession() as session:
            async with session.get(self.dump_url) as response:
                if response.status == 200:
                    with open(self.output_file, 'wb') as f:
                        f.write(await response.read())
                else:
                    raise Exception(f"Failed to download dump, status: {response.status}")
        
    def process(self) -> List[Transaction]:
        """Processes the dump file and returns a list of Transaction DTOs"""
        df = pd.read_csv(self.output_file, compression='gzip', sep='\t')

        if 'input_hex' in df.columns:
            df['input_hex'] = df['input_hex'].astype(str)

        transactions = df.to_dict(orient='records')

        transaction_dtos = [Transaction(**tx) for tx in transactions]
        return transaction_dtos

    async def get_last_processed_date(self) -> str:
        """Returns the last processed date from the Redis"""
        async with self.redis_pool.get_redis() as redis:
            date = await redis.get("last_processed_date")
            return date.decode("utf-8") if date else None

    async def set_last_processed_date(self, date: str) -> None:
        """Sets the last processed date in the Redis"""
        async with self.redis_pool.get_redis() as redis:
            await redis.set("last_processed_date", date)

    @staticmethod
    def get_next_date(current_date: str) -> str:
        """Returns the next date in the format YYYYMMDD"""
        current_date_obj = datetime.strptime(current_date, "%Y%m%d")
        next_date_obj = current_date_obj + timedelta(days=1)
        return next_date_obj.strftime("%Y%m%d")

    def cleanup(self) -> None:
        """Deletes the output file if it exists"""
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
            logger.info(f"File {self.output_file} has been deleted")
        else:
            logger.warning(f"File {self.output_file} does not exist for cleanup")
