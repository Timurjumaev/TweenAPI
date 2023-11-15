from pydantic import BaseModel, validator, Field
from db import SessionLocal
from models.collections import Collections
from utils.db_operations import get_in_db

db = SessionLocal()


class CreateCollection(BaseModel):
    model: str
    colour: str
    comment: str
    products_category_id: int = Field(..., gt=0)

    @validator('model')
    def model_validate(cls, v):
        validate_my = db.query(Collections).filter(
            Collections.model == v,
        ).count()

        if validate_my != 0:
            raise ValueError('Bunday nom aval ro`yxatga olingan!')
        return v


class UpdateCollection(BaseModel):
    id: int = Field(..., gt=0)
    model: str
    colour: str
    comment: str
    products_category_id: int = Field(..., gt=0)

    @validator('model')
    def model_validate(cls, v, values):
        validate_my = db.query(Collections).filter(
            Collections.model == v,
        ).count()

        the_item = get_in_db(db, Collections, values['id'])

        if validate_my != 0 and v != the_item.model:
            raise ValueError('Bunday nom aval ro`yxatga olingan!')
        return v

