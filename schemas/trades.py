from pydantic import BaseModel, Field


class CreateTrade(BaseModel):
    cell_id: int = Field(..., gt=0)
    amount: float = Field(..., gt=0)
    customer_id: int = Field(..., gt=0)
    discount: float = Field(..., ge=0)


class UpdateTrade(BaseModel):
    id: int = Field(..., gt=0)
    cell_id: int = Field(..., gt=0)
    amount: float = Field(..., gt=0)
    customer_id: int = Field(..., gt=0)
    discount: float = Field(..., ge=0)
