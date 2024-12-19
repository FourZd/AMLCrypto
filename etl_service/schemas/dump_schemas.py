from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Transaction(BaseModel):
    block_id: int
    index: Optional[str] = None
    hash: Optional[str] = None
    time: datetime
    failed: int
    type: str
    sender: Optional[str] = None
    recipient: str
    call_count: int
    value: str
    value_usd: float
    internal_value: str
    internal_value_usd: float
    fee: int
    fee_usd: float
    gas_used: int
    gas_limit: int
    gas_price: int
    input_hex: Optional[float] = None
    nonce: int
    v: Optional[float] = None
    r: Optional[float] = None
    s: Optional[float] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }