import os
from fastapi import HTTPException
from models.files import Files
from models.materials import Materials
from models.materials_categories import MaterialCategories
from models.users import Users
from models.workers import Workers
from utils.db_operations import get_in_db


def create_file(new_files, source, source_id, db):
    if (source == "worker" and db.query(Workers).filter(Workers.id == source_id).first() is None) or \
            (source == "user" and db.query(Users).filter(Users.id == source_id).first() is None) or \
            (source == "material" and db.query(Materials).filter(Materials.id == source_id).first() is None) or \
            (source == "materials_category" and db.query(MaterialCategories)
             .filter(MaterialCategories.id == source_id).first() is None):
        raise HTTPException(status_code=400, detail="File biriktiladigan obyekt topilamdi!")
    uploaded_file_objects = []

    for new_file in new_files:
        ext = os.path.splitext(new_file.filename)[-1].lower()
        if ext not in [".jpg", ".png", ".mp3", ".mp4", ".gif", ".jpeg"]:
            raise HTTPException(status_code=400, detail="Yuklanayotgan fayl formati mos kelmaydi!")
        file_location = f"files/{new_file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(new_file.file.read())

        new_item_db = Files(
            file=new_file.filename,
            source=source,
            source_id=source_id,
        )
        uploaded_file_objects.append(new_item_db)

    db.add_all(uploaded_file_objects)
    db.commit()


def delete_file(ident, db):
    get_in_db(db, Files, ident)
    db.query(Files).filter(Files.id == ident).delete()
    db.commit()


def update_file(new_files, source, source_id, db):
    items = db.query(Files).filter(Files.source == source,
                                   Files.source_id == source_id).all()
    for item in items:
        delete_file(item.id, db)
    create_file(new_files, source, source_id, db)
