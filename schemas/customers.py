from typing import List
from pydantic import BaseModel, Field
from schemas.phones import CreatePhone


class CreateCustomer(BaseModel):
    name: str
    phones: List[CreatePhone]


class UpdateCustomer(BaseModel):
    id: int = Field(..., gt=0)
    name: str
    phones: List[CreatePhone]
