from enum import Enum
from pydantic import BaseModel, Field


class SourceType(str, Enum):
    supply = "supply"
    stage_work = "stage_work"
    worker = "worker"
    other = "other"


class CreateExpense(BaseModel):
    source: SourceType
    source_id: int = Field(..., gt=0)
    money: float
    comment: str

