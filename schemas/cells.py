from pydantic import BaseModel, validator, Field
from db import SessionLocal
from models.cells import Cells
from utils.db_operations import get_in_db

db = SessionLocal()


class CreateCell(BaseModel):
    name: str
    price: float = Field(..., gt=0)

    @validator('name')
    def name_validate(cls, v):
        validate_my = db.query(Cells).filter(
            Cells.name == v,
        ).count()

        if validate_my != 0:
            raise ValueError('Bunday nom aval ro`yxatga olingan!')
        return v


class UpdateCell(BaseModel):
    id: int = Field(..., gt=0)
    name: str
    price: float = Field(..., gt=0)

    @validator('name')
    def name_validate(cls, v, values):
        validate_my = db.query(Cells).filter(
            Cells.name == v,
        ).count()

        the_item = get_in_db(db, Cells, values['id'])

        if validate_my != 0 and v != the_item.name:
            raise ValueError('Bunday nom aval ro`yxatga olingan!')
        return v

