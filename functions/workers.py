from datetime import datetime
from sqlalchemy.orm import joinedload
from functions.phones import create_phone, delete_phone
from models.phones import Phones
from models.workers import Workers
from utils.db_operations import get_in_db
from utils.pagination import pagination


def get_workers(ident, role, search, page, limit, db):

    if ident > 0:
        ident_filter = Workers.id == ident
    else:
        ident_filter = Workers.id > 0

    if role:
        role_filter = Workers.role == role
    else:
        role_filter = Workers.id > 0

    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Workers.name.like(search_formatted))
    else:
        search_filter = Workers.id > 0

    items = db.query(Workers).options(joinedload(Workers.phones), joinedload(Workers.files))\
        .filter(ident_filter, role_filter, search_filter).order_by(Workers.id.desc())

    return pagination(items, page, limit)


def create_worker(form, user, db):
    new_item_db = Workers(
        name=form.name,
        pay_type=form.pay_type,
        pay_amount=form.pay_amount,
        balance=0,
        role=form.role,
        date=datetime.today(),
        user_id=user.id
    )
    db.add(new_item_db)
    db.flush()
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(number, 'worker', new_item_db.id, comment, db, commit=False)
    db.commit()


def update_worker(form, user, db):
    get_in_db(db, Workers, form.id)
    db.query(Workers).filter(Workers.id == form.id).update({
        Workers.name: form.name,
        Workers.pay_type: form.pay_type,
        Workers.pay_amount: form.pay_amount,
        Workers.role: form.role,
        Workers.user_id: user.id
    })
    item_phones = db.query(Phones).filter(Phones.source_id == form.id,
                                          Phones.source == "worker").all()
    for phone in item_phones:
        delete_phone(phone.id, db)

    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(number, 'worker', form.id, comment, db, commit=False)
    db.commit()


def delete_worker(ident, db):
    get_in_db(db, Workers, ident)
    items = db.query(Phones).filter(Phones.source_id == ident,
                                    Phones.source == 'worker').all()
    for item in items:
        db.query(Phones).filter(Phones.id == item.id).delete()
    db.query(Workers).filter(Workers.id == ident).delete()
    db.commit()
