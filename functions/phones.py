from fastapi import HTTPException
from models.phones import Phones


def create_phone(number, source, source_id, comment, db, commit=True):
    if db.query(Phones).filter(Phones.number == number).count() > 0:
        raise HTTPException(status_code=422, detail="Bunday raqam avval ro`yxatga olingan!")
    new_phone_db = Phones(
        number=number,
        source=source,
        source_id=source_id,
        comment=comment,
    )
    db.add(new_phone_db)
    if commit:
        db.commit()


def delete_phone(id, db):
    db.query(Phones).filter(Phones.id == id).delete()
    db.commit()

