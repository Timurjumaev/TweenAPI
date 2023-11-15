from datetime import datetime
from db import Base
from sqlalchemy import Column, String, Integer, Numeric, Date


class Customers(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    balance = Column(Numeric, nullable=False)
    date = Column(Date, default=datetime.today(), nullable=False)

