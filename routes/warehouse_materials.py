import inspect
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from functions.warehouse_materials import get_warehouse_materials
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.users import CreateUser
from db import database


warehouse_materials_router = APIRouter(
    prefix="/warehouse_materials",
    tags=["Warehouse materials operation"]
)


@warehouse_materials_router.get('/get')
def get(ident: int = 0, search: str = None,  page: int = 1,
        limit: int = 25, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return get_warehouse_materials(ident, search, page, limit, db)
