from core.repositories import BaseRepository
from schemas import Transaction as TransactionSchema
from typing import List
from models import Transaction
from sqlalchemy.future import select
from mappers import TransactionMapper


class TransactionRepository(BaseRepository):

    async def get_existing_transaction_hashes(self, transaction_hashes: List[str]) -> List[str]:
        """
        Collects existing transaction hashes from the database
        
        Args:
            transaction_hashes (List[str]): List of transaction hashes to check
        
        Returns:
            List[str]: List of transaction hashes that are already in the database
        """
        async with self.get_session() as session:
            result = await session.execute(
                select(Transaction.hash).filter(Transaction.hash.in_(transaction_hashes))
            )
            existing_hashes = set(result.scalars())
            
            return existing_hashes
    
    async def add(
        self, transactions: List[TransactionSchema]  
    ) -> None:
        """
        Adds transactions to the database

        Args:
            transactions (List[TransactionSchema]): List of transactions to add
        """
        async with self.get_session() as session:
            async with session.begin():
                for transaction in transactions:
                    session.add(
                        TransactionMapper.from_schema_to_orm(transaction)
                    )


def repository_factory(session_factory):
    """Factory for creating a repository, injecting a dependency on the session factory"""
    return TransactionRepository(session_factory)