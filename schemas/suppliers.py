from typing import List
from pydantic import BaseModel, Field
from schemas.phones import CreatePhone


class CreateSupplier(BaseModel):
    name: str
    phones: List[CreatePhone]


class UpdateSupplier(BaseModel):
    id: int = Field(..., gt=0)
    name: str
    phones: List[CreatePhone]


