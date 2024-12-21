import pytest
from unittest.mock import AsyncMock
from transactions.services import TransactionService
from transactions.repositories import TransactionRepository
from transactions.schemas import TransactionSchema, TransactionStatsSchema

@pytest.fixture
def service():
    repository_mock = AsyncMock(spec=TransactionRepository)
    return TransactionService(transaction_repository=repository_mock)

@pytest.mark.asyncio
async def test_get_transactions(service):
    # Arrange
    service.transaction_repository.get_transactions.return_value = (
        [
            TransactionSchema(
                id=1,
                block_id=10,
                time="2024-12-21T12:00:00Z",
                recipient="0xRecipient",
                value=100,
                gas_limit=21000,
                nonce=1
            )
        ], 1
    )
    
    # Act
    transactions, count = await service.get_transactions(block_id=10, sender="0xSender", recipient=None, limit=10, offset=0)
    
    # Assert
    assert len(transactions) == 1
    assert transactions[0].id == 1
    assert count == 1

@pytest.mark.asyncio
async def test_get_transaction(service):
    # Arrange
    transaction = TransactionSchema(
        id=1,
        hash="0xHash",
        block_id=10,
        time="2024-12-21T12:00:00Z",
        recipient="0xRecipient",
        value=100,
        gas_limit=21000,
        nonce=1
    )
    service.transaction_repository.get_transaction.return_value = transaction
    
    # Act
    result = await service.get_transaction(transaction_hash="0xHash")
    
    # Assert
    assert result.id == 1

@pytest.mark.asyncio
async def test_get_transaction_not_found(service):
    # Arrange
    service.transaction_repository.get_transaction.return_value = None
    
    # Act & Assert
    with pytest.raises(ValueError, match="Transaction with hash 0xHash not found"):
        await service.get_transaction(transaction_hash="0xHash")

@pytest.mark.asyncio
async def test_get_transaction_stats(service):
    # Arrange
    service.transaction_repository.get_transaction_count.return_value = 100
    service.transaction_repository.get_average_gas_price.return_value = 12345
    
    # Act
    stats = await service.get_transaction_stats()
    
    # Assert
    assert stats.total_transactions == 100
    assert stats.average_gas_price == 12345
