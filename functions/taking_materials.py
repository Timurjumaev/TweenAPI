from sqlalchemy.orm import joinedload
from utils.db_operations import save_in_db
from utils.pagination import pagination
from models.taking_materials import TakingMaterials
from models.materials import Materials
from models.warehouse_materials import WarehouseMaterials
from fastapi import HTTPException


def get_taking_materials(ident, search, page, limit, material_id, db):

    if ident > 0:
        ident_filter = TakingMaterials.id == ident
    else:
        ident_filter = TakingMaterials.id > 0

    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Materials.name.like(search_formatted))
    else:
        search_filter = TakingMaterials.id > 0

    if material_id > 0:
        material_id_filter = TakingMaterials.material_id == material_id
    else:
        material_id_filter = TakingMaterials.id > 0

    items = (db.query(TakingMaterials).options(joinedload(TakingMaterials.material))
             .filter(ident_filter, search_filter, material_id_filter).order_by(TakingMaterials.id.desc()))

    return pagination(items, page, limit)


def create_taking_material(form, db):
    material = db.query(WarehouseMaterials).filter(WarehouseMaterials.material_id == form.material_id and
                                                   WarehouseMaterials.amount >= form.amount).first()
    if material is None:
        raise HTTPException(status_code=400, detail="Omborda mahsulot yetarli emas1")
    new_item_db = TakingMaterials(
        material_id=form.material_id,
        amount=form.amount
    )
    save_in_db(db, new_item_db)

    db.query(WarehouseMaterials).filter(WarehouseMaterials.id == material.id).update({
        WarehouseMaterials.amount: WarehouseMaterials.amount - form.amount
    })
    db.commit()
