import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.stage_works import get_stage_works, create_stage_work
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.users import CreateUser
from schemas.stage_works import CreateStageWork
from db import database


stage_works_router = APIRouter(
    prefix="/stage_works",
    tags=["StageWorks operation"]
)


@stage_works_router.get('/get')
def get(ident: int = 0, work_id: int = 0, stage_id: int = 0, worker_id: int = 0,
        search: str = None,  page: int = 1,
        limit: int = 25, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return get_stage_works(ident, work_id, stage_id, worker_id, search, page, limit, db)


@stage_works_router.post('/create')
def create(form: CreateStageWork, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_stage_work(form, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
