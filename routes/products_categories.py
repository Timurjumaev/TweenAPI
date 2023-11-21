import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.products_categories import get_products_categories, create_products_category, \
    update_products_category
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.products_categories import CreateProductsCategory, UpdateProductsCategory
from schemas.users import CreateUser
from db import database


products_categories_router = APIRouter(
    prefix="/products_categories",
    tags=["Product's Categories operation"]
)


@products_categories_router.get('/get')
def get(ident: int = 0, search: str = None,  page: int = 1,
        limit: int = 25, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return get_products_categories(ident, search, page, limit, db)


@products_categories_router.post('/create')
def create(form: CreateProductsCategory, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_products_category(form, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@products_categories_router.put("/update")
def update(form: UpdateProductsCategory, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_products_category(form, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")

