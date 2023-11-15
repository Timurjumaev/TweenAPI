from sqlalchemy.orm import joinedload
from models.materials_categories import MaterialCategories
from models.materials import Materials
from utils.db_operations import get_in_db, save_in_db
from utils.pagination import pagination


def get_materials(ident, search, page, limit, db):

    if ident > 0:
        ident_filter = Materials.id == ident
    else:
        ident_filter = Materials.id > 0

    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Materials.name.like(search_formatted),
                         Materials.measure.like(search_formatted),
                         MaterialCategories.name.like(search_formatted),
                         MaterialCategories.comment.like(search_formatted))
    else:
        search_filter = Materials.id > 0

    items = db.query(Materials).options(joinedload(Materials.materials_category), joinedload(Materials.files))\
        .filter(ident_filter, search_filter).order_by(Materials.id.desc())

    return pagination(items, page, limit)


def create_material(form, db):
    get_in_db(db, MaterialCategories, form.materials_category_id)
    new_item_db = Materials(
        name=form.name,
        measure=form.measure,
        materials_category_id=form.materials_category_id
    )
    save_in_db(db, new_item_db)


def update_material(form, db):
    get_in_db(db, MaterialCategories, form.materials_category_id)
    db.query(Materials).filter(Materials.id == form.id).update({
        Materials.name: form.name,
        Materials.measure: form.measure,
        Materials.materials_category_id: form.materials_category_id
    })
    db.commit()


def delete_material(ident, db):
    get_in_db(db, Materials, ident)
    db.query(Materials).filter(Materials.id == ident).delete()
    db.commit()
