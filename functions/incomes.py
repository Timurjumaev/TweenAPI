from sqlalchemy.orm import joinedload
from models.cells import Cells
from models.customers import Customers
from models.incomes import Incomes
from models.products import Products
from models.trades import Trades
from models.works import Works
from utils.db_operations import get_in_db, save_in_db
from utils.pagination import pagination
from models.stage_works import StageWorks
from fastapi import HTTPException


def get_incomes(ident, source, search, page, limit, db):

    if ident > 0:
        ident_filter = StageWorks.id == ident
    else:
        ident_filter = StageWorks.id > 0

    if source == "work":
        source_filter = Incomes.source == "work"
    elif source == "trade":
        source_filter = Incomes.source == "trade"
    else:
        source_filter = Incomes.id > 0

    if search:
        search_formatted = f"%{search}%"
        search_filter = (Customers.name.like(search_formatted) |
                         Products.model.like(search_formatted) |
                         Cells.name.like(search_formatted))
    else:
        search_filter = Incomes.id > 0

    items = (db.query(Incomes)
             .options(joinedload(Incomes.work).options(joinedload(Works.customer),
                                                       joinedload(Works.product),
                                                       joinedload(Works.cell)),
                      joinedload(Incomes.trade).options(joinedload(Trades.customer),
                                                        joinedload(Trades.cell)),
                      joinedload(Incomes.user))
             .filter(ident_filter, source_filter, search_filter).order_by(Incomes.id.desc()))

    return pagination(items, page, limit)


def create_income(form, user, db):

    if form.source == "work":
        work = get_in_db(db, Works, form.source_id)
        if work.type != "order":
            raise HTTPException(status_code=400, 
                                detail="Ushbu ish buyurtma emasligi sababli kirim qila olmaysiz!")
    elif form.source == "trade":
        get_in_db(db, Trades, form.source_id)

    new_item_db = Incomes(
        source=form.source,
        source_id=form.source_id,
        money=form.money,
        comment=form.comment,
        user_id=user.id
    )
    save_in_db(db, new_item_db)

    if new_item_db.source == "work":
        work = get_in_db(db, Works, new_item_db.source_id)
        db.query(Customers).filter(Customers.id == work.customer_id).update({
            Customers.balance: Customers.balance + new_item_db.money
        })

    elif new_item_db.source == "trade":
        trade = get_in_db(db, Trades, new_item_db.source_id)
        db.query(Customers).filter(Customers.id == trade.customer_id).update({
            Customers.balance: Customers.balance + new_item_db.money
        })

    db.commit()
