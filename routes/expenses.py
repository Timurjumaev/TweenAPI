import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.expenses import get_expenses, create_expense
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.users import CreateUser
from schemas.expenses import CreateExpense
from db import database


expenses_router = APIRouter(
    prefix="/expenses",
    tags=["Expenses operation"]
)


@expenses_router.get('/get')
def get(ident: int = 0, source: str = None, search: str = None,  page: int = 1,
        limit: int = 25, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return get_expenses(ident, source, search, page, limit, db)


@expenses_router.post('/create')
def create(form: CreateExpense, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_expense(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
