from core.schemas import CountSchema, StatusOkSchema
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from decimal import Decimal


class TransactionSchema(BaseModel):
    id: int
    block_id: int
    index: Optional[str] = None
    hash: Optional[str] = None
    time: datetime
    type: Optional[str] = None
    sender: Optional[str] = None
    recipient: str
    value: int
    fee: Optional[int] = None
    gas_limit: int
    gas_price: Optional[int] = None
    input_hex: Optional[str] = None
    nonce: int

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class TransactionStatsSchema(BaseModel):
    total_transactions: int
    average_gas_price: Decimal


class GetTransactionResponse(StatusOkSchema):
    data: TransactionSchema


class GetTransactionsResponse(StatusOkSchema, CountSchema):
    data: List[TransactionSchema]


class GetTransactionStatsResponse(StatusOkSchema):
    data: TransactionStatsSchema