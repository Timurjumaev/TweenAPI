from sqlalchemy.orm import joinedload
from functions.phones import create_phone, delete_phone
from models.phones import Phones
from routes.login import get_password_hash
from utils.db_operations import get_in_db
from utils.pagination import pagination
from models.users import Users
from fastapi import HTTPException


def get_users(ident, search, page, limit, db):

    if ident > 0:
        ident_filter = Users.id == ident
    else:
        ident_filter = Users.id > 0

    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Users.name.like(search_formatted) |
                         Users.username.like(search_formatted))
    else:
        search_filter = Users.id > 0

    items = db.query(Users).options(joinedload(Users.phones), joinedload(Users.files))\
        .filter(ident_filter, search_filter).order_by(Users.id.desc())

    return pagination(items, page, limit)


def create_user(form, db):
    new_item_db = Users(
        name=form.name,
        username=form.username,
        role=form.role,
        password=get_password_hash(form.password))
    db.add(new_item_db)
    db.flush()
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(number, 'user', new_item_db.id, comment, db, commit=False)
    db.commit()


def update_user(form, db):
    get_in_db(db, Users, form.id)
    db.query(Users).filter(Users.id == form.id).update({
        Users.name: form.name,
        Users.username: form.username,
        Users.password: get_password_hash(form.password),
        Users.role: form.role,
    })

    item_phones = db.query(Phones).filter(Phones.source_id == form.id,
                                          Phones.source == "user").all()
    for phone in item_phones:
        delete_phone(phone.id, db)

    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(number, 'user', form.id, comment, db, commit=False)
    db.commit()


def delete_user(ident, db):
    get_in_db(db, Users, ident)
    items = db.query(Phones).filter(Phones.source_id == ident,
                                    Phones.source == 'user').all()
    for item in items:
        db.query(Phones).filter(Phones.id == item.id).delete()
    db.query(Users).filter(Users.id == ident).delete()
    db.commit()


def create_permission_f(form, db):
    user = get_in_db(db, Users, form.id)
    if user.role != "admin":
        raise HTTPException(status_code=400, detail="Bossga ruxsat qo'sha olmaysiz!")
    db.query(Users).filter(Users.id == user.id).update({
        Users.permissions: form.permissions
    })
    db.commit()

