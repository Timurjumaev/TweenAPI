from sqlalchemy.orm import joinedload
from models.products import Products
from models.products_categories import ProductsCategories
from utils.db_operations import get_in_db, save_in_db
from utils.pagination import pagination


def get_products(ident, search, page, limit, category_id, db):

    if ident > 0:
        ident_filter = Products.id == ident
    else:
        ident_filter = Products.id > 0

    if search:
        # search_formatted = "%{}%".format(search)
        search_formatted = f"%{search}%"
        search_filter = (Products.model.like(search_formatted),
                         Products.comment.like(search_formatted),
                         ProductsCategories.name.like(search_formatted),
                         ProductsCategories.comment.like(search_formatted))
    else:
        search_filter = Products.id > 0

    if category_id > 0:
        category_filter = Products.products_category_id == category_id
    else:
        category_filter = Products.id > 0

    items = db.query(Products).options(joinedload(Products.products_category), joinedload(Products.files))\
        .filter(ident_filter, category_filter).order_by(Products.id.desc())

    return pagination(items, page, limit)


def create_product(form, db):
    get_in_db(db, ProductsCategories, form.products_category_id)
    new_item_db = Products(
        size=form.size,
        model=form.model,
        colour=form.colour,
        amount=0,
        comment=form.comment,
        products_category_id=form.products_category_id,
        price1=form.price1,
        price2=form.price2,
        price3=form.price3
    )
    save_in_db(db, new_item_db)


def update_product(form, db):
    get_in_db(db, Products, form.id), get_in_db(db, ProductsCategories, form.products_category_id)
    db.query(Products).filter(Products.id == form.id).update({
        Products.size: form.size,
        Products.model: form.model,
        Products.colour: form.colour,
        Products.comment: form.comment,
        Products.products_category_id: form.products_category_id,
        Products.price1: form.price1,
        Products.price2: form.price2,
        Products.price3: form.price3,
    })
    db.commit()

