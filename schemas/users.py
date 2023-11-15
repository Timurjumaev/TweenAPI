from enum import Enum
from typing import List
from pydantic import BaseModel, validator, Field
from models.users import Users
from schemas.phones import CreatePhone
from db import SessionLocal
from utils.db_operations import get_in_db

db = SessionLocal()


class RoleType(str, Enum):
    admin = "admin"
    boss = "boss"


class CreateUser(BaseModel):
    name: str
    username: str
    password: str
    role: RoleType
    phones: List[CreatePhone]

    @validator('username')
    def username_validate(cls, username):
        validate_my = db.query(Users).filter(
            Users.username == username,
        ).count()

        if validate_my != 0:
            raise ValueError('Bunday login aval ro`yxatga olingan!')
        return username

    @validator('password')
    def password_validate(cls, password):
        if len(password) < 8:
            raise ValueError('Parol 8 tadan kam bo`lmasligi kerak')
        return password


class UpdateUser(BaseModel):
    id: int = Field(..., gt=0)
    name: str
    username: str
    password: str
    role: str
    phones: List[CreatePhone]

    @validator('username')
    def username_validate(cls, username, values):
        validate_my = db.query(Users).filter(
            Users.username == username,
        ).count()

        the_user = get_in_db(db, Users, values['id'])

        if validate_my != 0 and username != the_user.username:
            raise ValueError('Bunday login aval ro`yxatga olingan!')
        return username

    @validator('password')
    def password_validate(cls, password):
        if len(password) < 8:
            raise ValueError('Parol 8 tadan kam bo`lmasligi kerak')
        return password
