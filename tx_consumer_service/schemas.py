from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Transaction(BaseModel):
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

