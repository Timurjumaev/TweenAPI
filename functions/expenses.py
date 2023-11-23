from sqlalchemy.orm import joinedload
from models.expenses import Expenses
from models.materials import Materials
from models.suppliers import Suppliers
from models.supplies import Supplies
from models.workers import Workers
from utils.db_operations import get_in_db, save_in_db
from utils.pagination import pagination
from models.stage_works import StageWorks


def get_expenses(ident, source, search, page, limit, db):

    if ident > 0:
        ident_filter = StageWorks.id == ident
    else:
        ident_filter = StageWorks.id > 0

    if source == "supply":
        source_filter = Expenses.source == "supply"
    elif source == "stage_work":
        source_filter = Expenses.source == "stage_work"
    elif source == "worker":
        source_filter = Expenses.source == "worker"
    else:
        source_filter = Expenses.id > 0

    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Suppliers.name.like(search_formatted) |
                         Materials.name.like(search_formatted) |
                         Workers.name.like(search_formatted))
    else:
        search_filter = Expenses.id > 0

    items = (db.query(Expenses)
             .options(joinedload(Expenses.supply).options(joinedload(Supplies.supplier),
                                                          joinedload(Supplies.material)),
                      joinedload(Expenses.stage_work),
                      joinedload(Expenses.worker),
                      joinedload(Expenses.user))
             .filter(ident_filter, source_filter, search_filter).order_by(Expenses.id.desc()))

    return pagination(items, page, limit)


def create_expense(form, user, db):

    if form.source == "supply":
        get_in_db(db, Supplies, form.source_id)
    elif form.source == "stage_work":
        get_in_db(db, StageWorks, form.source_id)
    elif form.source == "worker":
        get_in_db(db, Workers, form.source_id)

    new_item_db = Expenses(
        source=form.source,
        source_id=form.source_id,
        money=form.money,
        comment=form.comment,
        user_id=user.id
    )
    save_in_db(db, new_item_db)

    if new_item_db.source == "supply":
        supply = get_in_db(db, Supplies, new_item_db.source_id)
        db.query(Suppliers).filter(Suppliers.id == supply.supplier_id).update({
            Suppliers.balance: Suppliers.balance - new_item_db.money
        })

    elif new_item_db.source == "stage_work":
        stage_work = get_in_db(db, StageWorks, new_item_db.source_id)
        db.query(Workers).filter(Workers.id == stage_work.worker_id).update({
            Workers.balance: Workers.balance - new_item_db.money
        })

    elif new_item_db.source == "worker":
        db.query(Workers).filter(Workers.id == new_item_db.source_id).update({
            Workers.balance: Workers.balance - new_item_db.money
        })

    db.commit()
