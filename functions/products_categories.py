from sqlalchemy.orm import joinedload
from models.products_categories import ProductsCategories
from utils.db_operations import get_in_db, save_in_db
from utils.pagination import pagination


def get_products_categories(ident, search, page, limit, db):

    if ident > 0:
        ident_filter = ProductsCategories.id == ident
    else:
        ident_filter = ProductsCategories.id > 0

    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (ProductsCategories.name.like(search_formatted) |
                         ProductsCategories.comment.like(search_formatted))
    else:
        search_filter = ProductsCategories.id > 0

    items = db.query(ProductsCategories).options(joinedload(ProductsCategories.files))\
        .filter(ident_filter, search_filter).order_by(ProductsCategories.id.desc())

    return pagination(items, page, limit)


def create_products_category(form, db):
    new_item_db = ProductsCategories(
        name=form.name,
        comment=form.comment
    )
    save_in_db(db, new_item_db)


def update_products_category(form, db):
    get_in_db(db, ProductsCategories, form.id)
    db.query(ProductsCategories).filter(ProductsCategories.id == form.id).update({
        ProductsCategories.name: form.name,
        ProductsCategories.comment: form.comment
    })
    db.commit()
