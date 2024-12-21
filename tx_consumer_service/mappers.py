from schemas import Transaction as TransactionSchema
from models import Transaction


class TransactionMapper:
    
    @staticmethod
    def from_schema_to_orm(transaction_dto: TransactionSchema) -> Transaction:
        """
        Convert transaction DTO (pydantic schema) to transaction ORM model
        """
        return Transaction(
            block_id=transaction_dto.block_id,
            index=transaction_dto.index,
            hash=transaction_dto.hash,
            time=transaction_dto.time,
            type=transaction_dto.type,
            sender=transaction_dto.sender,
            recipient=transaction_dto.recipient,
            value=str(transaction_dto.value),
            fee=str(transaction_dto.fee),
            gas_limit=transaction_dto.gas_limit,
            gas_price=transaction_dto.gas_price,
            input_hex=transaction_dto.input_hex,
            nonce=transaction_dto.nonce,
        )