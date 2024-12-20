from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, BigInteger, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from core.database import BaseModel


class Transaction(BaseModel):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    block_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    index: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    hash: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    sender: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    recipient: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[int] = mapped_column(BigInteger, nullable=False)
    fee: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    gas_limit: Mapped[int] = mapped_column(BigInteger, nullable=False)
    gas_price: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    input_hex: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    nonce: Mapped[int] = mapped_column(Integer, nullable=False)
