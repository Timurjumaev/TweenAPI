from datetime import datetime
from sqlalchemy.orm import joinedload
from functions.phones import create_phone, delete_phone
from models.phones import Phones
from utils.db_operations import get_in_db
from utils.pagination import pagination
from models.customers import Customers


def get_customers(ident, search, page, limit, db):

    if ident > 0:
        ident_filter = Customers.id == ident
    else:
        ident_filter = Customers.id > 0

    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Customers.name.like(search_formatted))
    else:
        search_filter = Customers.id > 0

    items = db.query(Customers).options(joinedload(Customers.phones).load_only(Phones.number, Phones.comment))\
        .filter(ident_filter, search_filter).order_by(Customers.id.desc())

    return pagination(items, page, limit)


def create_customer(form, db):
    new_item_db = Customers(
        name=form.name,
        balance=0,
        date=datetime.today())
    db.add(new_item_db)
    db.flush()
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(number, 'customer', new_item_db.id, comment, db, commit=False)
    db.commit()


def update_customer(form, db):
    get_in_db(db, Customers, form.id)
    db.query(Customers).filter(Customers.id == form.id).update({
        Customers.name: form.name,
    })
    item_phones = db.query(Phones).filter(Phones.source_id == form.id,
                                          Phones.source == "customer").all()
    for phone in item_phones:
        delete_phone(phone.id, db)

    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(number, 'customer', form.id, comment, db, commit=False)
    db.commit()


def delete_customer(ident, db):
    get_in_db(db, Customers, ident)
    items = db.query(Phones).filter(Phones.source_id == ident,
                                    Phones.source == 'customer').all()
    for item in items:
        db.query(Phones).filter(Phones.id == item.id).delete()
    db.query(Customers).filter(Customers.id == ident).delete()
    db.commit()
