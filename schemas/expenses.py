from enum import Enum
from pydantic import BaseModel, Field


class MeasureType(str, Enum):
    dona = "dona"
    kilogram = "kilogram"
    metr = "metr"


class CreateExpense(BaseModel):
    name: str
    measure: MeasureType
    materials_category_id: int = Field(..., gt=0)
