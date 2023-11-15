import inspect
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from functions.files import create_file, update_file, delete_file
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.files import CreateFile
from schemas.users import CreateUser
from db import database


files_router = APIRouter(
    prefix="/files",
    tags=["Files operation"]
)


@files_router.post("/create")
async def create(
    form: CreateFile = Depends(CreateFile),
    db: Session = Depends(database),
    current_user: CreateUser = Depends(get_current_active_user)
):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_file(form.new_files, form.source, form.source_id, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@files_router.put("/update")
async def update(
    form: CreateFile = Depends(CreateFile),
    db: Session = Depends(database),
    current_user: CreateUser = Depends(get_current_active_user)
):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_file(form.new_files, form.source, form.source_id, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@files_router.delete("/delete")
def delete(ident: int, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_file(ident, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
