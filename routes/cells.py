import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.cells import get_cells, create_cell, update_cell
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.cells import UpdateCell, CreateCell
from schemas.users import CreateUser
from db import database


cells_router = APIRouter(
    prefix="/cells",
    tags=["Cells operation"]
)


@cells_router.get('/get')
def get(ident: int = 0, search: str = None,  page: int = 1,
        limit: int = 25, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return get_cells(ident, search, page, limit, db)


@cells_router.post('/create')
def create(form: CreateCell, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_cell(form, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@cells_router.put("/update")
def update(form: UpdateCell, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_cell(form, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")

