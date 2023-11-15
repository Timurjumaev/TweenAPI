from datetime import datetime
from sqlalchemy.orm import joinedload
from functions.phones import create_phone, delete_phone
from models.phones import Phones
from models.suppliers import Suppliers
from utils.db_operations import get_in_db
from utils.pagination import pagination


def get_suppliers(ident, search, page, limit, db):

    if ident > 0:
        ident_filter = Suppliers.id == ident
    else:
        ident_filter = Suppliers.id > 0

    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Suppliers.name.like(search_formatted))
    else:
        search_filter = Suppliers.id > 0

    items = db.query(Suppliers).options(joinedload(Suppliers.phones))\
        .filter(ident_filter, search_filter).order_by(Suppliers.id.desc())

    return pagination(items, page, limit)


def create_supplier(form, user, db):
    new_item_db = Suppliers(
        name=form.name,
        balance=0,
        date=datetime.today(),
        user_id=user.id
    )
    db.add(new_item_db)
    db.flush()
    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(number, 'supplier', new_item_db.id, comment, db, commit=False)
    db.commit()


def update_supplier(form, user, db):
    get_in_db(db, Suppliers, form.id)
    db.query(Suppliers).filter(Suppliers.id == form.id).update({
        Suppliers.name: form.name,
        Suppliers.user_id: user.id
    })

    item_phones = db.query(Phones).filter(Phones.source_id == form.id,
                                          Phones.source == "supplier").all()
    for phone in item_phones:
        delete_phone(phone.id, db)

    for i in form.phones:
        comment = i.comment
        number = i.number
        create_phone(number, 'supplier', form.id, comment, db, commit=False)
    db.commit()


def delete_supplier(ident, db):
    get_in_db(db, Suppliers, ident)
    items = db.query(Phones).filter(Phones.source_id == ident,
                                    Phones.source == 'supplier').all()
    for item in items:
        db.query(Phones).filter(Phones.id == item.id).delete()
    db.query(Suppliers).filter(Suppliers.id == ident).delete()
    db.commit()
