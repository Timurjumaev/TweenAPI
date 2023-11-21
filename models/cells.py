from db import Base
from sqlalchemy import Column, String, Integer, Numeric


class Cells(Base):
    __tablename__ = 'cells'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    price = Column(Numeric, nullable=False)
