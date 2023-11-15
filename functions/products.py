from sqlalchemy.orm import joinedload
from models.collections import Collections
from models.products import Products
from utils.db_operations import get_in_db, save_in_db
from utils.pagination import pagination


def get_products(ident, search, page, limit, db):

    if ident > 0:
        ident_filter = Products.id == ident
    else:
        ident_filter = Products.id > 0

    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Products.name.like(search_formatted),
                         Products.measure.like(search_formatted),
                         Collections.model.like(search_formatted),
                         Collections.comment.like(search_formatted))
    else:
        search_filter = Products.id > 0

    items = db.query(Products).options(joinedload(Products.collection), joinedload(Products.files))\
        .filter(ident_filter, search_filter).order_by(Products.id.desc())

    return pagination(items, page, limit)


def create_product(form, db):
    get_in_db(db, Collections, form.collection_id)
    new_item_db = Products(
        size=form.size,
        comment=form.comment,
        collection_id=form.collection_id
    )
    save_in_db(db, new_item_db)


def update_product(form, db):
    get_in_db(db, Products, form.id)
    get_in_db(db, Collections, form.collection_id)
    db.query(Products).filter(Products.id == form.id).update({
        Products.size: form.size,
        Products.comment: form.comment,
        Products.collection_id: form.collection_id
    })
    db.commit()


def delete_product(ident, db):
    get_in_db(db, Products, ident)
    db.query(Products).filter(Products.id == ident).delete()
    db.commit()
