import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.materials_categories import get_materials_categories, create_materials_category, \
    update_materials_category, delete_material_category
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.materials_categories import CreateMaterialsCategory, UpdateMaterialsCategory
from schemas.users import CreateUser
from db import database


materials_categories_router = APIRouter(
    prefix="/materials_categories",
    tags=["Material's Categories operation"]
)


@materials_categories_router.get('/get')
def get(ident: int = 0, search: str = None,  page: int = 1,
        limit: int = 25, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return get_materials_categories(ident, search, page, limit, db)


@materials_categories_router.post('/create')
def create(form: CreateMaterialsCategory, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_materials_category(form, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@materials_categories_router.put("/update")
def update(form: UpdateMaterialsCategory, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_materials_category(form, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@materials_categories_router.delete("/delete")
def delete(ident: int = 0, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_material_category(ident, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
