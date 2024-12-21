from core.repositories import BaseRepository
from schemas import Transaction as TransactionSchema
from typing import List
from models import Transaction
from sqlalchemy.future import select
from mappers import TransactionMapper


class TransactionRepository(BaseRepository):

    async def get_existing_transaction_hashes(self, transaction_hashes: List[str]) -> List[str]:
        """Получить список хешей транзакций, которые уже есть в базе"""
        async with self.get_session() as session:
            result = await session.execute(
                select(Transaction.hash).filter(Transaction.hash.in_(transaction_hashes))
            )
            existing_hashes = set(result.scalars())
            
            return existing_hashes
    
    async def add(
        self, transactions: List[TransactionSchema]  
    ) -> None:
        """В идеале было бы добавлять транзакции в репозитории по одной и просто контролировать атомарность извне с UoW
        Но в случае тестового задания, я надеюсь что мне простят пару сэкономленных часов :)"""
        async with self.get_session() as session:
            async with session.begin():
                for transaction in transactions:
                    session.add(
                        TransactionMapper.from_schema_to_orm(transaction)
                    )


def repository_factory(session_factory):
    """Фабрика для создания репозитория, внедряя зависимость от сессии"""
    return TransactionRepository(session_factory)