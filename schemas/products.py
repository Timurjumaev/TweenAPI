from pydantic import BaseModel, Field


class CreateProduct(BaseModel):
    size: str
    comment: str
    collection_id: int = Field(..., gt=0)


class UpdateProduct(BaseModel):
    id: int = Field(..., gt=0)
    size: str
    comment: str
    collection_id: int = Field(..., gt=0)


