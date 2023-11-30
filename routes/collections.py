import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.collections import get_collections, create_collection, \
    update_collection, delete_collection
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.collections import CreateCollection, UpdateCollection
from schemas.users import CreateUser
from db import database


collections_router = APIRouter(
    prefix="/collections",
    tags=["Collections operation"]
)


@collections_router.get('/get')
def get(ident: int = 0, search: str = None,  page: int = 1,
        limit: int = 25, category_id: int = 0, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return get_collections(ident, search, page, limit, category_id, db)


@collections_router.post('/create')
def create(form: CreateCollection, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_collection(form, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@collections_router.put("/update")
def update(form: UpdateCollection, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_collection(form, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@collections_router.delete("/delete")
def delete(ident: int = 0, db: Session = Depends(database),
           current_user: CreateUser = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_collection(ident, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
