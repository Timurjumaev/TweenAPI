from pydantic import BaseModel, validator, Field
from db import SessionLocal
from models.products import Products
from utils.db_operations import get_in_db

db = SessionLocal()


class CreateProduct(BaseModel):
    size: str
    model: str
    colour: str
    comment: str
    products_category_id: int = Field(..., gt=0)
    price1: int = Field(..., gt=0)
    price2: int = Field(..., gt=0)
    price3: int = Field(..., gt=0)

    @validator('model')
    def model_validate(cls, v):
        validate_my = db.query(Products).filter(
            Products.model == v,
        ).count()

        if validate_my != 0:
            raise ValueError('Bunday nom aval ro`yxatga olingan!')
        return v


class UpdateProduct(BaseModel):
    id: int = Field(..., gt=0)
    size: str
    model: str
    colour: str
    comment: str
    products_category_id: int = Field(..., gt=0)
    price1: int = Field(..., gt=0)
    price2: int = Field(..., gt=0)
    price3: int = Field(..., gt=0)

    @validator('model')
    def model_validate(cls, v, values):
        validate_my = db.query(Products).filter(
            Products.model == v,
        ).count()

        the_item = get_in_db(db, Products, values['id'])

        if validate_my != 0 and v != the_item.model:
            raise ValueError('Bunday nom aval ro`yxatga olingan!')
        return v



