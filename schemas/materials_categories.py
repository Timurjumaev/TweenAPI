from pydantic import BaseModel, validator, Field
from db import SessionLocal
from models.materials_categories import MaterialCategories
from utils.db_operations import get_in_db

db = SessionLocal()


class CreateMaterialsCategory(BaseModel):
    name: str
    comment: str

    @validator('name')
    def username_validate(cls, v):
        validate_my = db.query(MaterialCategories).filter(
            MaterialCategories.name == v,
        ).count()

        if validate_my != 0:
            raise ValueError('Bunday nom aval ro`yxatga olingan!')
        return v


class UpdateMaterialsCategory(BaseModel):
    id: int = Field(..., gt=0)
    name: str
    comment: str

    @validator('name')
    def username_validate(cls, v, values):
        validate_my = db.query(MaterialCategories).filter(
            MaterialCategories.name == v,
        ).count()

        the_item = get_in_db(db, MaterialCategories, values['id'])

        if validate_my != 0 and v != the_item.name:
            raise ValueError('Bunday nom aval ro`yxatga olingan!')
        return v
