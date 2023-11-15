from db import Base
from sqlalchemy import Column, String, Integer


class Stages(Base):
    __tablename__ = 'stages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    number = Column(Integer, nullable=False)

