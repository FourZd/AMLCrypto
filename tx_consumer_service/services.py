from repositories import TransactionRepository
from schemas import Transaction as TransactionSchema
from typing import List


class TransactionService:
    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    async def get_existing_transaction_hashes(self, transaction_hashes: List[str]) -> List[str]:
        """Получить список хешей транзакций, которые уже есть в базе"""
        return await self.transaction_repository.get_existing_transaction_hashes(transaction_hashes)

    async def add(self, transactions: List[TransactionSchema]) -> None:
        """Добавить транзакции в базу"""
        await self.transaction_repository.add(transactions)


def service_factory(transaction_repository: TransactionRepository):
    """Фабрика для создания сервиса, внедряя зависимость от репозитория"""
    return TransactionService(transaction_repository)