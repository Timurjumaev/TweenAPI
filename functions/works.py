from sqlalchemy.orm import joinedload

from models.cells import Cells
from models.works import Works
from models.products import Products
from models.stages import Stages
from models.customers import Customers
from utils.db_operations import get_in_db, save_in_db
from utils.pagination import pagination
from fastapi import HTTPException


def get_works(ident, page, limit, type, product_id, stage_id, cell_id, status, stage_status, db):

    if ident > 0:
        ident_filter = Works.id == ident
    else:
        ident_filter = Works.id > 0

    if type == "work":
        type_filter = Works.type == "work"
    elif type == "order":
        type_filter = Works.type == "order"
    else:
        type_filter = Works.id > 0

    if product_id > 0:
        product_id_filter = Works.product_id == product_id
    else:
        product_id_filter = Works.id > 0

    if stage_id > 0:
        stage_filter = Works.stage_id == stage_id
    else:
        stage_filter = Works.id > 0

    if cell_id > 0:
        cell_filter = Works.cell_id == cell_id
    else:
        cell_filter = Works.id > 0

    if status:
        status_filter = Works.status
    else:
        status_filter = Works.id > 0

    if stage_status:
        stage_status_filter = Works.stage_status
    else:
        stage_status_filter = Works.id > 0

    items = (db.query(Works).options(joinedload(Works.product),
                                     joinedload(Works.user),
                                     joinedload(Works.stage),
                                     joinedload(Works.customer),
                                     joinedload(Works.cell))
             .filter(ident_filter,type_filter, product_id_filter, stage_filter, status_filter, stage_status_filter, cell_filter)
             .order_by(Works.id.desc()))

    return pagination(items, page, limit)


def create_work(form, user, db):
    get_in_db(db, Products, form.product_id)
    stage = db.query(Stages).filter(Stages.number == 1).first()
    if stage is None:
        raise HTTPException(status_code=400, detail="Avval 1-bosqichni qo'shing!")
    if form.type == "work":
        price = 0
        customer_id = 0
    else:
        price = form.price
        customer_id = form.customer_id
        get_in_db(db, Customers, form.customer_id)
    new_item_db = Works(
        type=form.type,
        product_id=form.product_id,
        amount=form.amount,
        comment=form.comment,
        user_id=user.id,
        stage_id=stage.id,
        price=price,
        customer_id=customer_id
    )
    save_in_db(db, new_item_db)


def finish_stage(ident, db):
    work = get_in_db(db, Works, ident)
    if work.status:
        raise HTTPException(status_code=400, detail="Ushbu ish allaqachon yakunlangan")
    db.query(Works).filter(Works.id == work.id).update({
        Works.stage_status: True
    })
    db.commit()


def next_stage(work_ident, stage_ident, db):
    new_stage = get_in_db(db, Stages, stage_ident)
    work = get_in_db(db, Works, work_ident)
    current_stage = get_in_db(db, Stages, work.stage_id)
    if new_stage.number <= current_stage.number:
        raise HTTPException(status_code=400, detail="Bosqichni ortga qaytara olmaysiz!")
    if work.status:
        raise HTTPException(status_code=400, detail="Ushbu ish allaqachon yakunlangan")
    if not work.stage_status:
        raise HTTPException(status_code=400, detail="Ushbu ish bosqichi hali yakunlanmagan")
    db.query(Works).filter(Works.id == work.id).update({
        Works.stage_id: stage_ident,
        Works.stage_status: False
    })
    db.commit()


def update_work(form, user, db):
    work = get_in_db(db, Works, form.id)
    get_in_db(db, Products, form.product_id), get_in_db(db, Customers, form.customer_id)
    if work.stage_status:
        raise HTTPException(status_code=400, detail="Ish bosqichi allaqachon yakunlangan!")
    db.query(Works).filter(Works.id == form.id).update({
        Works.type: form.type,
        Works.product_id: form.product_id,
        Works.amount: form.amount,
        Works.comment: form.comment,
        Works.user_id: user.id,
        Works.price: form.price,
        Works.customer_id: form.customer_id
    })
    db.commit()


def delete_work(ident, db):
    work = get_in_db(db, Works, ident)
    stage = db.query(Stages).filter(Stages.id == work.stage_id).first()
    if stage.number != 1 or work.stage_status:
        raise HTTPException(status_code=400, detail="Boshlangan ishni o'chira olmaysiz")
    db.query(Works).filter(Works.id == ident).delete()
    db.commit()


def confirmation_work(form, db):
    work = get_in_db(db, Works, form.id)
    if work.cell_id:
        raise HTTPException(status_code=400, detail="Ushbu ish allaqachon yakunlangan!")
    get_in_db(db, Cells, form.cell_id)
    db.query(Works).filter(Works.id == work.id).update({
        Works.cell_id == form.cell_id
    })
    db.commit()
