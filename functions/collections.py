from sqlalchemy.orm import joinedload

from models.products import Products
from models.products_categories import ProductsCategories
from models.collections import Collections
from utils.db_operations import get_in_db, save_in_db
from utils.pagination import pagination


def get_collections(ident, search, page, limit, category_id, db):

    if ident > 0:
        ident_filter = Collections.id == ident
    else:
        ident_filter = Collections.id > 0

    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Collections.model.like(search_formatted),
                         Collections.colour.like(search_formatted),
                         Collections.comment.like(search_formatted),
                         ProductsCategories.name.like(search_formatted),
                         ProductsCategories.comment.like(search_formatted))
    else:
        search_filter = Collections.id > 0

    if category_id > 0:
        category_filter = Collections.products_category_id == category_id
    else:
        category_filter = Collections.id > 0

    items = db.query(Collections).options(joinedload(Collections.products_category), joinedload(Collections.files))\
        .filter(ident_filter, search_filter, category_filter).order_by(Collections.id.desc())

    return pagination(items, page, limit)


def create_collection(form, db):
    get_in_db(db, ProductsCategories, form.products_category_id)
    new_item_db = Collections(
        model=form.model,
        colour=form.colour,
        amount=0,
        comment=form.comment,
        products_category_id=form.products_category_id
    )
    save_in_db(db, new_item_db)


def update_collection(form, db):
    get_in_db(db, ProductsCategories, form.products_category_id)
    db.query(Collections).filter(Collections.id == form.id).update({
        Collections.model: form.model,
        Collections.colour: form.colour,
        Collections.comment: form.comment,
        Collections.products_category_id: form.products_category_id
    })
    db.commit()


def delete_collection(ident, db):
    get_in_db(db, Collections, ident)
    items = db.query(Products).filter(Products.collection_id == ident).all()
    for item in items:
        db.query(Products).filter(Products.id == item.id).delete()
    db.query(Collections).filter(Collections.id == ident).delete()
    db.commit()
