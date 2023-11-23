from sqlalchemy.orm import joinedload

from models.products import Products
from utils.db_operations import get_in_db, save_in_db
from utils.pagination import pagination
from models.stage_works import StageWorks
from models.works import Works
from models.stages import Stages
from models.workers import Workers


def get_stage_works(ident, work_id, stage_id, worker_id, search, page, limit, db):

    if ident > 0:
        ident_filter = StageWorks.id == ident
    else:
        ident_filter = StageWorks.id > 0

    if work_id > 0:
        work_filter = StageWorks.work_id == work_id
    else:
        work_filter = StageWorks.id > 0

    if stage_id > 0:
        stage_filter = StageWorks.stage_id == stage_id
    else:
        stage_filter = StageWorks.id > 0

    if worker_id > 0:
        worker_filter = StageWorks.worker_id == worker_id
    else:
        worker_filter = StageWorks.id > 0

    if search:
        search_formatted = f"%{search}%"
        search_filter = (Workers.name.like(search_formatted))
    else:
        search_filter = StageWorks.id > 0

    items = db.query(StageWorks).options(joinedload(StageWorks.work), joinedload(StageWorks.stage),
                                         joinedload(StageWorks.worker))\
        .filter(ident_filter, work_filter, stage_filter, worker_filter, search_filter).order_by(StageWorks.id.desc())

    return pagination(items, page, limit)


def create_stage_work(form, db):

    work = get_in_db(db, Works, form.work_id)
    stage = get_in_db(db, Stages, form.stage_id)
    worker = get_in_db(db, Workers, form.worker_id)
    product = get_in_db(db, Products, work.product_id)

    new_item_db = StageWorks(
        work_id=form.work_id,
        stage_id=form.stage_id,
        worker_id=form.worker_id,
        amount=form.amount,
        bonus=form.bonus
    )
    save_in_db(db, new_item_db)

    if stage.number == 1:
        money = product.price1
    elif stage.number == 2:
        money = product.price2
    elif stage.number == 3:
        money = product.price3
    else:
        money = 0

    if new_item_db.bonus > 0:
        money += new_item_db.bonus

    db.query(Workers).filter(Workers.id == worker.id).update({
        Workers.balance: Workers.balance + (money * new_item_db.amount)
    })
    db.commit()




