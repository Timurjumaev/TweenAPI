from models.stages import Stages
from utils.db_operations import save_in_db


def get_stages(db):
    return db.query(Stages).order_by(Stages.id).all()


def create_stage(form, db):
    new_item_db = Stages(
        name=form.name,
        number=form.number
    )
    save_in_db(db, new_item_db)


