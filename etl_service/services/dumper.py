import aiohttp
import os
from urllib.parse import urlparse
import pandas as pd
from typing import List
from schemas.dump_schemas import Transaction


class Dumper:

    def __init__(self, dump_url: str, output_dir: str):
        self.dump_url = dump_url
        self.output_dir = output_dir

        self.file_name = os.path.basename(urlparse(self.dump_url).path)
        self.output_file = os.path.join(self.output_dir, self.file_name)

        os.makedirs(self.output_dir, exist_ok=True)

    async def download(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.dump_url) as response:
                if response.status == 200:
                    with open(self.output_file, 'wb') as f:
                        f.write(await response.read())
                else:
                    raise Exception(f"Failed to download dump, status: {response.status}")
        
    def process(self) -> List[Transaction]:
        df = pd.read_csv(self.output_file, compression='gzip', sep='\t')
        transactions = df.to_dict(orient='records')
        transaction_dtos = [Transaction(**tx) for tx in transactions]
        return transaction_dtos

