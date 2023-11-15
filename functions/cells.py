from models.cells import Cells
from utils.db_operations import save_in_db
from utils.pagination import pagination


def get_cells(ident, search, page, limit, db):

    if ident > 0:
        ident_filter = Cells.id == ident
    else:
        ident_filter = Cells.id > 0

    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Cells.name.like(search_formatted))
    else:
        search_filter = Cells.id > 0

    items = db.query(Cells).filter(ident_filter, search_filter).order_by(Cells.id.desc())

    return pagination(items, page, limit)


def create_cell(name, db):
    new_item_db = Cells(
        name=name,
    )
    save_in_db(db, new_item_db)


def update_cell(form, db):
    db.query(Cells).filter(Cells.id == form.id).update({
        Cells.name: form.name,
    })
    db.commit()
