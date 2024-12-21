from repositories import TransactionRepository
from schemas import Transaction as TransactionSchema
from typing import List


class TransactionService:
    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    async def get_existing_transaction_hashes(self, transaction_hashes: List[str]) -> List[str]:
        """
        Gets existing transaction hashes from the database
        
        Args:
            transaction_hashes (List[str]): List of transaction hashes to check
        
        Returns:
            List[str]: List of transaction hashes that are already in the database
        """
        return await self.transaction_repository.get_existing_transaction_hashes(transaction_hashes)

    async def add(self, transactions: List[TransactionSchema]) -> None:
        """Adds transactions to the database"""
        await self.transaction_repository.add(transactions)


def service_factory(transaction_repository: TransactionRepository):
    """Factory for creating a service, injecting a dependency on the repository"""
    return TransactionService(transaction_repository)