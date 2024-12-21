import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from transactions.repositories import TransactionRepository
from transactions.models import Transaction

@pytest.fixture
def repository():
    # Mock session and session factory
    session_mock = AsyncMock(spec=AsyncSession)
    session_context_mock = MagicMock()
    session_context_mock.__aenter__.return_value = session_mock
    session_context_mock.__aexit__.return_value = None

    # Mock repository
    repository = TransactionRepository(session_factory=MagicMock(return_value=session_context_mock))
    return repository

@pytest.mark.asyncio
async def test_get_transactions(repository):
    # Arrange
    transaction = Transaction(id=1, block_id=10, sender="0xSender", recipient="0xRecipient", hash="0xHash")
    session_mock = repository.session_factory.return_value.__aenter__.return_value
    session_mock.execute.return_value.scalars.return_value.all.return_value = [transaction]
    session_mock.execute.return_value.scalar.return_value = 1
    
    # Act
    transactions, count = await repository.get_transactions(block_id=10, sender="0xSender", recipient=None, limit=10, offset=0)
    
    # Assert
    assert len(transactions) == 1
    assert transactions[0].id == 1
    assert count == 1

@pytest.mark.asyncio
async def test_get_transaction(repository):
    # Arrange
    transaction = Transaction(id=1, hash="0xHash")
    session_mock = repository.session_factory.return_value.__aenter__.return_value
    session_mock.execute.return_value.scalar.return_value = transaction
    
    # Act
    result = await repository.get_transaction(transaction_hash="0xHash")
    
    # Assert
    assert result.id == 1
    assert result.hash == "0xHash"

@pytest.mark.asyncio
async def test_get_transaction_count(repository):
    # Arrange
    session_mock = repository.session_factory.return_value.__aenter__.return_value
    session_mock.execute.return_value.scalar.return_value = 42
    
    # Act
    count = await repository.get_transaction_count()
    
    # Assert
    assert count == 42

@pytest.mark.asyncio
async def test_get_average_gas_price(repository):
    # Arrange
    session_mock = repository.session_factory.return_value.__aenter__.return_value
    session_mock.execute.return_value.scalar.return_value = 12345
    
    # Act
    avg_gas_price = await repository.get_average_gas_price()
    
    # Assert
    assert avg_gas_price == 12345
