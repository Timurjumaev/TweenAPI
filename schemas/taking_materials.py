from pydantic import BaseModel, Field


class CreateTakingMaterial(BaseModel):
    material_id: int = Field(..., gt=0)
    amount: float = Field(..., gt=0)
