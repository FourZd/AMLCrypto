from core.repositories import BaseRepository
from .models import Transaction
from .mappers import TransactionMapper
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List, Tuple, Optional
from .schemas import TransactionSchema


class TransactionRepository(BaseRepository):

    async def get_transactions(self, block_id: int, sender: str, recipient: str, limit: int, offset: int) -> Tuple[List[TransactionSchema], int]:
        async with self.get_session() as session:

            base_query = select(Transaction)
            
            if block_id:
                base_query = base_query.where(Transaction.block_id == block_id)
            if sender:
                base_query = base_query.where(Transaction.sender == sender)
            if recipient:
                base_query = base_query.where(Transaction.recipient == recipient)
            
            count_query = base_query.with_only_columns(func.count())
            count_result = await session.execute(count_query)
            count = count_result.scalar()
            
            paginated_query = base_query.limit(limit).offset(offset).order_by(Transaction.id.desc())
            result = await session.execute(paginated_query)
            transaction_entities = result.scalars().all()
            transactions = [TransactionMapper.from_orm_to_schema(tx) for tx in transaction_entities]

            return transactions, count

    async def get_transaction(self, transaction_hash: str) -> Optional[TransactionSchema]:
        async with self.get_session() as session:
            query = select(Transaction).where(Transaction.hash == transaction_hash)
            result = await session.execute(query)
            transaction_entity = result.scalar()
            if not transaction_entity:
                return None
            return TransactionMapper.from_orm_to_schema(transaction_entity)
        
    async def get_transaction_count(self) -> int:
        async with self.get_session() as session:
            query = select(func.count(Transaction.id))
            result = await session.execute(query)
            return result.scalar()
        
    async def get_average_gas_price(self) -> int:
        async with self.get_session() as session:
            query = select(func.avg(Transaction.gas_price))
            result = await session.execute(query)
            return result.scalar()