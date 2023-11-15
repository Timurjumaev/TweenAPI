from enum import Enum
from pydantic import BaseModel, validator, Field
from db import SessionLocal
from models.materials import Materials
from utils.db_operations import get_in_db

db = SessionLocal()


class MeasureType(str, Enum):
    dona = "dona"
    kilogram = "kilogram"
    metr = "metr"


class CreateMaterial(BaseModel):
    name: str
    measure: MeasureType
    materials_category_id: int = Field(..., gt=0)

    @validator('name')
    def name_validate(cls, v):
        validate_my = db.query(Materials).filter(
            Materials.name == v,
        ).count()

        if validate_my != 0:
            raise ValueError('Bunday nom aval ro`yxatga olingan!')
        return v


class UpdateMaterial(BaseModel):
    id: int = Field(..., gt=0)
    name: str
    measure: MeasureType
    materials_category_id: int = Field(..., gt=0)

    @validator('name')
    def name_validate(cls, v, values):
        validate_my = db.query(Materials).filter(
            Materials.name == v,
        ).count()

        the_item = get_in_db(db, Materials, values['id'])

        if validate_my != 0 and v != the_item.name:
            raise ValueError('Bunday nom aval ro`yxatga olingan!')
        return v

