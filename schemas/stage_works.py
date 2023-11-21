from pydantic import BaseModel, Field


class CreateStageWork(BaseModel):
    work_id: int = Field(..., gt=0)
    stage_id: int = Field(..., gt=0)
    worker_id: int = Field(..., gt=0)
    amount: int = Field(..., gt=0)
    bonus: int = Field(..., ge=0)
