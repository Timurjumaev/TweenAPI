import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.trades import get_trades, create_trade, update_trade, confirmation_trade
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.trades import CreateTrade, UpdateTrade
from schemas.users import CreateUser
from db import database


trades_router = APIRouter(
    prefix="/trades",
    tags=["Trades operation"]
)


@trades_router.get('/get')
def get(ident: int = 0, cell_id: int = 0, customer_id: int = 0,
        status: bool = True, search: str = None,  page: int = 1,
        limit: int = 25, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return get_trades(ident, cell_id, customer_id, status, search, page, limit, db)


@trades_router.post('/create')
def create(form: CreateTrade, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_trade(form, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@trades_router.put("/update")
def update(form: UpdateTrade, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_trade(form, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@trades_router.patch("/confirmation")
def confirmation(ident: int = 0, db: Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    confirmation_trade(ident, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
