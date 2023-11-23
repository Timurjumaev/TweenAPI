import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.incomes import get_incomes, create_income
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.users import CreateUser
from schemas.incomes import CreateIncome
from db import database


incomes_router = APIRouter(
    prefix="/incomes",
    tags=["Incomes operation"]
)


@incomes_router.get('/get')
def get(ident: int = 0, source: str = None, search: str = None,  page: int = 1,
        limit: int = 25, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return get_incomes(ident, source, search, page, limit, db)


@incomes_router.post('/create')
def create(form: CreateIncome, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_income(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
