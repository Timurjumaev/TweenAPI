from enum import Enum
from pydantic import BaseModel, Field


class Type(str, Enum):
    work = "work"
    order = "order"


class CreateWork(BaseModel):
    type: Type
    product_id: int = Field(..., gt=0)
    amount: int = Field(..., gt=0)
    comment: str
    price: float
    customer_id: int


class UpdateWork(BaseModel):
    id: int = Field(..., gt=0)
    type: Type
    product_id: int = Field(..., gt=0)
    amount: int = Field(..., gt=0)
    comment: str
    price: float
    customer_id: int


class FinishWork(BaseModel):
    id: int = Field(..., gt=0)
    cell_id: int


