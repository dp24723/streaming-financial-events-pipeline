from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class FinancialEvent(BaseModel):
    event_id: str
    event_time: datetime
    account_id: str
    symbol: str = Field(min_length=1, max_length=10)
    side: Literal["BUY", "SELL"]
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)

    @field_validator("symbol", "currency")
    @classmethod
    def uppercase(cls, value: str) -> str:
        return value.upper()

    @property
    def amount(self) -> float:
        signed = self.quantity * self.price
        return signed if self.side == "BUY" else -signed
