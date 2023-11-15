import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.supplies import get_supplies, create_supply, \
    update_supply, delete_supply, confirmation_supply
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.supplies import CreateSupply, UpdateSupply
from schemas.users import CreateUser
from db import database


supplies_router = APIRouter(
    prefix="/supplies",
    tags=["Supplies operation"]
)


@supplies_router.get('/get')
def get(ident: int = 0, search: str = None,  page: int = 1,
        limit: int = 25, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return get_supplies(ident, search, page, limit, db)


@supplies_router.post('/create')
def create(form: CreateSupply, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return create_supply(form, current_user, db)
    # raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@supplies_router.put("/update")
def update(form: UpdateSupply, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_supply(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@supplies_router.delete("/delete")
def delete(ident: int = 0, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_supply(ident, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@supplies_router.put("/confirmation",
                     description="Ixtiyoriy omborga tasdiqlanmaga ta'minotning "
                                 "ID si kiritiladi va shu ID li ta'minot omborga saqlanadi")
def confirmation(ident: int = 0, db: Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    confirmation_supply(ident, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
