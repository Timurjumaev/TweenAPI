import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.workers import get_workers, create_worker, update_worker, delete_worker
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.workers import CreateWorker, UpdateWorker
from schemas.users import CreateUser
from db import database


workers_router = APIRouter(
    prefix="/workers",
    tags=["Workers operation"]
)


@workers_router.get('/get')
def get(ident: int = 0, role: str = None, search: str = None,  page: int = 1,
        limit: int = 25, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return get_workers(ident, role, search, page, limit, db)


@workers_router.post('/create')
def create(form: CreateWorker, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_worker(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@workers_router.put("/update")
def update(form: UpdateWorker, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_worker(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@workers_router.delete("/delete")
def delete(ident: int = 0, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_worker(ident, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
