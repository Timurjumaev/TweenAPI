from datetime import datetime
from db import Base
from sqlalchemy import Column, String, Integer, Numeric, Date


class Workers(Base):
    __tablename__ = 'workers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    pay_type = Column(String(255), nullable=False)
    pay_amount = Column(Numeric, nullable=False)
    balance = Column(Numeric, nullable=False)
    role = Column(Numeric, nullable=False)
    date = Column(Date, default=datetime.today(), nullable=False)
    user_id = Column(Integer, nullable=False)
