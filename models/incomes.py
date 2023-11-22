from datetime import datetime
from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import Column, String, Integer, Numeric, Date, and_
from models.trades import Trades
from models.users import Users
from models.works import Works


class Incomes(Base):
    __tablename__ = 'incomes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(255), nullable=False)
    source_id = Column(Integer, nullable=False)
    money = Column(Numeric, nullable=False)
    comment = Column(String(255), nullable=True)
    date = Column(Date, default=datetime.today(), nullable=False)
    user_id = Column(Integer, nullable=False)

    work = relationship('Works', foreign_keys=[source_id],
                        primaryjoin=lambda: and_(Works.id == Incomes.source_id, Incomes.source == "work"))

    trade = relationship('Trades', foreign_keys=[source_id],
                         primaryjoin=lambda: and_(Trades.id == Incomes.source_id, Incomes.source == "trade"))

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Incomes.user_id))
