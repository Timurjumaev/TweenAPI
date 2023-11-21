import inspect
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from functions.works import get_works, create_work, update_work, delete_work, finish_stage, next_stage, confirmation_work
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.works import CreateWork, UpdateWork, FinishWork
from schemas.users import CreateUser
from db import database


works_router = APIRouter(
    prefix="/works",
    tags=["Works operation"]
)


@works_router.get('/get')
def get(ident: int = 0, type: str = None, product_id: int = 0,  page: int = 1,
        stage_id: int = 0, cell_id: int = 0, status: bool = False, stage_status: bool = False,
        limit: int = 25, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return get_works(ident, page, limit, type, product_id, stage_id, cell_id, status, stage_status, db)


@works_router.post('/create')
def create(form: CreateWork, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_work(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@works_router.patch("/finish_stage")
def finish(ident: int = 0, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    finish_stage(ident, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@works_router.patch("/next_stage")
def next(work_ident: int = Query(0), stage_ident: int = Query(0), db: Session = Depends(database),
         current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    next_stage(work_ident, stage_ident, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@works_router.put("/update")
def update(form: UpdateWork, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_work(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@works_router.delete("/delete")
def delete(ident: int = 0, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_work(ident, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@works_router.patch("/confirmation")
def confirmation(form: FinishWork, db: Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    confirmation_work(form, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
