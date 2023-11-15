import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.stages import get_stages, create_stage
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.users import CreateUser
from schemas.stages import CreateStage
from db import database


stages_router = APIRouter(
    prefix="/stages",
    tags=["Stages operation"]
)


@stages_router.get('/get')
def get(db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return get_stages(db)


@stages_router.post('/create')
def create(form: CreateStage, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_stage(form, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
