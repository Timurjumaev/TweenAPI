from enum import Enum
from pydantic import BaseModel, Field


class SourceType(str, Enum):
    work = "work"
    trade = "trade"


class CreateIncome(BaseModel):
    source: SourceType
    source_id: int = Field(..., gt=0)
    money: float
    comment: str
