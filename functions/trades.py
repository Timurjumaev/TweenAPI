from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from utils.db_operations import get_in_db, save_in_db
from utils.pagination import pagination
from models.cells import Cells
from models.customers import Customers
from models.trades import Trades


def get_trades(ident, cell_id, customer_id, status, search, page, limit, db):

    if ident > 0:
        ident_filter = Trades.id == ident
    else:
        ident_filter = Trades.id > 0

    if cell_id > 0:
        cell_filter = Trades.id == cell_id
    else:
        cell_filter = Trades.id > 0

    if customer_id > 0:
        customer_filter = Trades.id == customer_id
    else:
        customer_filter = Trades.id > 0

    if status:
        status_filter = Trades.status == True
    else:
        status_filter = Trades.status == False

    if search:
        search_formatted = f"%{search}%"
        search_filter = (Customers.name.like(search_formatted),
                         Cells.name.like(search_formatted))
    else:
        search_filter = Trades.id > 0

    items = db.query(Trades).options(joinedload(Trades.customer), joinedload(Trades.cell))\
        .filter(ident_filter, cell_filter, customer_filter, status_filter, search_filter).order_by(Trades.id.desc())

    return pagination(items, page, limit)


def create_trade(form, db, user):
    get_in_db(db, Cells, form.cell_id), get_in_db(db, Customers, form.customer_id)
    new_item_db = Trades(
        cell_id=form.cell_id,
        amount=form.amount,
        customer_id=form.customer_id,
        user_id=user.id,
        status=False,
        discount=form.discount
    )
    save_in_db(db, new_item_db)


def update_trade(form, db, user):
    trade = get_in_db(db, Trades, form.id)
    if trade.status:
        raise HTTPException(status_code=400, detail="Ushbu savdo allaqachon yakunlangan!")
    get_in_db(db, Cells, form.cell_id), get_in_db(db, Customers, form.customer_id)
    db.query(Trades).filter(Trades.id == form.id).update({
        Trades.cell_id: form.cell_id,
        Trades.amount: form.amount,
        Trades.customer_id: form.customer_id,
        Trades.date: datetime.today(),
        Trades.user_id: user.id,
        Trades.discount: form.discount
    })
    db.commit()


def confirmation_trade(ident, db):
    get_in_db(db, Trades, ident)
    db.query(Trades).filter(Trades.id == ident).update({
        Trades.status: True
    })
    db.commit()
