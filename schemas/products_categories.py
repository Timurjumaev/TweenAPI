from pydantic import BaseModel, validator, Field
from db import SessionLocal
from models.products_categories import ProductsCategories
from utils.db_operations import get_in_db

db = SessionLocal()


class CreateProductsCategory(BaseModel):
    name: str
    comment: str

    @validator('name')
    def name_validate(cls, v):
        validate_my = db.query(ProductsCategories).filter(
            ProductsCategories.name == v,
        ).count()

        if validate_my != 0:
            raise ValueError('Bunday nom aval ro`yxatga olingan!')
        return v


class UpdateProductsCategory(BaseModel):
    id: int = Field(..., gt=0)
    name: str
    comment: str

    @validator('name')
    def name_validate(cls, v, values):
        validate_my = db.query(ProductsCategories).filter(
            ProductsCategories.name == v,
        ).count()

        the_item = get_in_db(db, ProductsCategories, values['id'])

        if validate_my != 0 and v != the_item.name:
            raise ValueError('Bunday nom aval ro`yxatga olingan!')
        return v
