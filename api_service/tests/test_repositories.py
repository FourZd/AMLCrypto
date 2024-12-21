import asyncio
from typing import List
from unittest.mock import AsyncMock

from sqlalchemy import func

from core.repositories import BaseRepository
from transactions.schemas import TransactionSchema
from transactions.mappers import TransactionMapper
from datetime import datetime


class MockData:
    transactions: List[TransactionSchema] = [
        TransactionSchema(
            id=1,
            hash="tx1_hash",
            block_id=1,
            sender="alice",
            recipient="bob",
            gas_price=100,
            time=datetime(2024, 12, 21, 12, 0, 0),  # Use datetime object
            value=1000,
            gas_limit=21000,
            nonce=0,
            fee=10,  # Add fee
            input_hex="0x00", # Add input_hex
        ),
        TransactionSchema(
            id=2,
            hash="tx2_hash",
            block_id=2,
            sender="bob",
            recipient="charlie",
            gas_price=200,
            time=datetime(2024, 12, 21, 12, 0, 0),  # Use datetime object
            value=1200,
            gas_limit=25000,
            nonce=1,
            fee=20,  # Add fee
            input_hex="0x01", # Add input_hex
        ),
    ]


class MockedTransactionRepository(BaseRepository):
    def __init__(self, session: AsyncMock = None):
        super().__init__(session_factory=AsyncMock())
        self.session = session or AsyncMock()
        self.transactions = MockData.transactions

    async def get_session(self, session: AsyncMock = None):
        return self.session

    async def _execute_scalar(self, query):  # Вспомогательная функция
        result_mock = AsyncMock()
        result_mock.scalar.return_value = query.compile(compile_kwargs={"literal_binds": True})
        self.session.execute.return_value = result_mock
        return await self.session.execute(query)


async def test_get_transactions_all():
    session_mock = AsyncMock()
    session_mock.execute.return_value = AsyncMock(scalars=AsyncMock(return_value=MockData.transactions))
    session_mock.execute.return_value.scalar.return_value = len(MockData.transactions)

    repository = MockedTransactionRepository(session_mock)
    transactions, count = await repository.get_transactions(None, None, None, 10, 0)

    assert transactions == MockData.transactions
    assert count == len(MockData.transactions)


async def test_get_transactions_filtered():
    session_mock = AsyncMock()
    filtered_transactions = [tx for tx in MockData.transactions if tx.block_id == 2 and tx.sender == "alice"]
    session_mock.execute.return_value = AsyncMock(scalars=AsyncMock(return_value=filtered_transactions))
    session_mock.execute.return_value.scalar.return_value = len(filtered_transactions)

    repository = MockedTransactionRepository(session_mock)
    transactions, count = await repository.get_transactions(2, "alice", None, 10, 0)

    assert transactions == filtered_transactions
    assert count == len(filtered_transactions)


async def test_get_transaction_by_hash():
    session_mock = AsyncMock()
    session_mock.execute.return_value = AsyncMock(scalar=AsyncMock(return_value=MockData.transactions[0]))

    repository = MockedTransactionRepository(session_mock)
    transaction = await repository.get_transaction("tx1_hash")

    assert transaction == MockData.transactions[0]


async def test_get_transaction_by_hash_not_found():
    session_mock = AsyncMock()
    session_mock.execute.return_value = AsyncMock(scalar=None)

    repository = MockedTransactionRepository(session_mock)
    transaction = await repository.get_transaction("nonexistent_hash")

    assert transaction is None


async def test_get_transaction_count():
    session_mock = AsyncMock()
    session_mock.execute.return_value = AsyncMock(scalar=AsyncMock(return_value=len(MockData.transactions)))
    repository = MockedTransactionRepository(session_mock)
    count = await repository.get_transaction_count()
    assert count == len(MockData.transactions)


async def test_get_average_gas_price():
    session_mock = AsyncMock()
    avg_gas_price = sum(tx.gas_price for tx in MockData.transactions) / len(MockData.transactions)
    session_mock.execute.return_value = AsyncMock(scalar=AsyncMock(return_value=avg_gas_price))
    repository = MockedTransactionRepository(session_mock)
    avg = await repository.get_average_gas_price()
    assert avg == avg_gas_price