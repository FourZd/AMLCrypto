from transactions.repositories import TransactionRepository
from typing import List, Tuple
from transactions.schemas import TransactionSchema, TransactionStatsSchema


class TransactionService:
    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    async def get_transactions(
            self, block_id: int, sender: str, recipient: str, limit: int, offset: int
    ) -> Tuple[List[TransactionSchema], int]:
        return await self.transaction_repository.get_transactions(block_id, sender, recipient, limit, offset)

    async def get_transaction(self, transaction_hash: str) -> TransactionSchema:
        transaction = await self.transaction_repository.get_transaction(transaction_hash)
        if not transaction:
            raise ValueError(f"Transaction with hash {transaction_hash} not found")
        return transaction
    
    async def get_transaction_stats(self) -> TransactionStatsSchema:
        tx_count = await self.transaction_repository.get_transaction_count()
        avg_gas_price = await self.transaction_repository.get_average_gas_price()
        return TransactionStatsSchema(total_transactions=tx_count, average_gas_price=avg_gas_price)