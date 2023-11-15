from pydantic import BaseModel, Field


class CreateStage(BaseModel):
    name: str
    number: int = Field(..., gt=0)
