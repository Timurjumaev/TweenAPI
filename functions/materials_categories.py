from sqlalchemy.orm import joinedload

from models.materials import Materials
from models.materials_categories import MaterialCategories
from utils.db_operations import get_in_db, save_in_db
from utils.pagination import pagination


def get_materials_categories(ident, search, page, limit, db):

    if ident > 0:
        ident_filter = MaterialCategories.id == ident
    else:
        ident_filter = MaterialCategories.id > 0

    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (MaterialCategories.name.like(search_formatted) |
                         MaterialCategories.comment.like(search_formatted))
    else:
        search_filter = MaterialCategories.id > 0

    items = db.query(MaterialCategories).options(joinedload(MaterialCategories.files))\
        .filter(ident_filter, search_filter).order_by(MaterialCategories.id.desc())

    return pagination(items, page, limit)


def create_materials_category(form, db):
    new_item_db = MaterialCategories(
        name=form.name,
        comment=form.comment
    )
    save_in_db(db, new_item_db)


def update_materials_category(form, db):
    get_in_db(db, MaterialCategories, form.id)
    db.query(MaterialCategories).filter(MaterialCategories.id == form.id).update({
        MaterialCategories.name: form.name,
        MaterialCategories.comment: form.comment
    })
    db.commit()


def delete_material_category(ident, db):
    get_in_db(db, MaterialCategories, ident)
    items = db.query(Materials).filter(Materials.materials_category_id == ident).all()
    for item in items:
        db.query(Materials).filter(Materials.id == item.id).delete()
    db.query(MaterialCategories).filter(MaterialCategories.id == ident).delete()
    db.commit()
