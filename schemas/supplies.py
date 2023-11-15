from pydantic import BaseModel, Field


class CreateSupply(BaseModel):
    material_id: int = Field(..., gt=0)
    supplier_id: int = Field(..., gt=0)
    amount: float = Field(..., gt=0)
    price: float = Field(..., gt=0)


class UpdateSupply(BaseModel):
    id: int = Field(..., gt=0)
    material_id: int = Field(..., gt=0)
    supplier_id: int = Field(..., gt=0)
    amount: float = Field(..., gt=0)
    price: float = Field(..., gt=0)

