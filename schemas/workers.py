from enum import Enum
from typing import List
from pydantic import BaseModel, Field
from schemas.phones import CreatePhone


class PayType(str, Enum):
    kpi = "kpi"
    salary = "salary"


class RoleType(str, Enum):
    one = "1"
    two = "2"
    three = "3"
    four = "4"


class CreateWorker(BaseModel):
    name: str
    pay_type: PayType
    pay_amount: float = Field(..., gt=0)
    role: RoleType
    phones: List[CreatePhone]


class UpdateWorker(BaseModel):
    id: int = Field(..., gt=0)
    name: str
    pay_type: PayType
    pay_amount: float = Field(..., gt=0)
    role: RoleType
    phones: List[CreatePhone]
