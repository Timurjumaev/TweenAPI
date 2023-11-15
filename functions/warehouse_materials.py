from sqlalchemy.orm import joinedload
from models.materials import Materials
from models.materials_categories import MaterialCategories
from models.warehouse_materials import WarehouseMaterials
from utils.pagination import pagination


def get_warehouse_materials(ident, search, page, limit, db):

    if ident > 0:
        ident_filter = WarehouseMaterials.id == ident
    else:
        ident_filter = WarehouseMaterials.id > 0

    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Materials.name.like(search_formatted),
                         Materials.measure.like(search_formatted),
                         MaterialCategories.name.like(search_formatted),
                         MaterialCategories.comment.like(search_formatted))
    else:
        search_filter = WarehouseMaterials.id > 0

    items = db.query(WarehouseMaterials)\
        .options(joinedload(WarehouseMaterials.material).subqueryload(Materials.materials_category))\
        .filter(ident_filter, search_filter).order_by(WarehouseMaterials.id.desc())

    return pagination(items, page, limit)
