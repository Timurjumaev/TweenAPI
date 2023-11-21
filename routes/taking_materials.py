import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.taking_materials import get_taking_materials, create_taking_material
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.users import CreateUser
from schemas.taking_materials import CreateTakingMaterial
from db import database


taking_materials_router = APIRouter(
    prefix="/taking_materials",
    tags=["TakingMaterials operation"]
)


@taking_materials_router.get('/get')
def get(ident: int = 0, search: str = None,  page: int = 1,
        limit: int = 25, material_id: int = 0, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return get_taking_materials(ident, search, page, limit, material_id, db)


@taking_materials_router.post('/create')
def create(form: CreateTakingMaterial, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_taking_material(form, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")