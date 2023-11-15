from fastapi import UploadFile
from typing import List
from pydantic import BaseModel, Field
from enum import Enum


class SourceType(str, Enum):
    user = "user"
    worker = "worker"
    material = "material"
    materials_category = "materials_category"


class CreateFile(BaseModel):
    new_files: List[UploadFile]
    source: SourceType
    source_id: int = Field(..., gt=0)
