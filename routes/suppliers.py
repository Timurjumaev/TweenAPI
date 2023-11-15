import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.suppliers import get_suppliers, create_supplier, update_supplier, delete_supplier
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.suppliers import CreateSupplier, UpdateSupplier
from schemas.users import CreateUser
from db import database


suppliers_router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers operation"]
)


@suppliers_router.get('/get')
def get(ident: int = 0, search: str = None,  page: int = 1,
        limit: int = 25, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return get_suppliers(ident, search, page, limit, db)


@suppliers_router.post('/create')
def create(form: CreateSupplier, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_supplier(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@suppliers_router.put("/update")
def update(form: UpdateSupplier, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_supplier(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@suppliers_router.delete("/delete")
def delete(ident: int = 0, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_supplier(ident, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
