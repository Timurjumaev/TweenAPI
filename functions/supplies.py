from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from models.materials import Materials
from models.suppliers import Suppliers
from models.supplies import Supplies
from models.users import Users
from models.warehouse_materials import WarehouseMaterials
from utils.db_operations import get_in_db, save_in_db
from utils.pagination import pagination


def get_supplies(ident, search, page, limit, db):

    if ident > 0:
        ident_filter = Supplies.id == ident
    else:
        ident_filter = Supplies.id > 0

    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Materials.name.like(search_formatted) |
                         Suppliers.name.like(search_formatted) |
                         Users.name.like(search_formatted))
    else:
        search_filter = Supplies.id > 0

    items = db.query(Supplies).options(joinedload(Supplies.material),
                                       joinedload(Supplies.supplier),
                                       joinedload(Supplies.user))\
        .filter(ident_filter, search_filter).order_by(Supplies.id.desc())

    return pagination(items, page, limit)


def create_supply(form, user, db):
    get_in_db(db, Materials, form.material_id), get_in_db(db, Suppliers, form.supplier_id)
    new_item_db = Supplies(
        material_id=form.material_id,
        supplier_id=form.supplier_id,
        amount=form.amount,
        price=form.price,
        status=False,
        date=datetime.today(),
        user_id=user.id
    )
    save_in_db(db, new_item_db)
    return new_item_db


def update_supply(form, user, db):
    the_supply = get_in_db(db, Supplies, form.id)
    if the_supply.status:
        raise HTTPException(status_code=400, detail="Tanlangan mahsulot omborga qo'shilgan!")
    get_in_db(db, Materials, form.material_id), get_in_db(db, Suppliers, form.supplier_id)
    db.query(Supplies).filter(Supplies.id == form.id).update({
        Supplies.material_id: form.material_id,
        Supplies.supplier_id: form.supplier_id,
        Supplies.amount: form.amount,
        Supplies.price: form.price,
        Supplies.date: datetime.today(),
        Supplies.user_id: user.id
    })
    db.commit()


def delete_supply(ident, db):
    the_supply = get_in_db(db, Supplies, ident)
    if the_supply.status:
        raise HTTPException(status_code=400, detail="Tanlangan mahsulot omborga qo'shilgan!")
    db.query(Materials).filter(Materials.id == ident).delete()
    db.commit()


def confirmation_supply(ident, user, db):
    the_supply = get_in_db(db, Supplies, ident)
    db.query(Supplies).filter(Supplies.id == ident).update({
        Supplies.status: True,
        Supplies.date: datetime.today(),
        Supplies.user_id: user.id
    })
    the_warehouse_product = db.query(WarehouseMaterials).filter(
        WarehouseMaterials.material_id == the_supply.material_id,
        WarehouseMaterials.price == the_supply.price
    ).first()
    if the_warehouse_product:
        db.query(WarehouseMaterials).filter(WarehouseMaterials.id == the_warehouse_product.id).update({
            WarehouseMaterials.amount: WarehouseMaterials.amount + the_supply.amount
        })
    new_item_db = WarehouseMaterials(
        material_id=the_supply.material_id,
        amount=the_supply.amount,
        price=the_supply.price
    )
    db.add(new_item_db)
    db.query(Suppliers).filter(Suppliers.id == the_supply.supplier_id).update({
        Suppliers.balance: Suppliers.balance + the_supply.price * the_supply.amount
    })
    db.commit()
