from .schemas import TransactionSchema
from .models import Transaction


class TransactionMapper:

    @staticmethod
    def from_orm_to_schema(transaction: Transaction) -> TransactionSchema:
        return TransactionSchema(
            id=transaction.id,
            block_id=transaction.block_id,
            index=transaction.index,
            hash=transaction.hash,
            time=transaction.time,
            type=transaction.type,
            sender=transaction.sender,
            recipient=transaction.recipient,
            value=transaction.value,
            fee=transaction.fee,
            gas_limit=transaction.gas_limit,
            gas_price=transaction.gas_price,
            input_hex=transaction.input_hex,
            nonce=transaction.nonce
        )