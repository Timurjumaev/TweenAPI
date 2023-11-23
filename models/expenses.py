from datetime import datetime
from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import Column, String, Integer, Numeric, Date, and_
from models.supplies import Supplies
from models.users import Users
from models.stage_works import StageWorks
from models.workers import Workers


class Expenses(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(255), nullable=False)
    source_id = Column(Integer, nullable=False)
    money = Column(Numeric, nullable=False)
    comment = Column(String(255), nullable=True)
    date = Column(Date, default=datetime.today(), nullable=False)
    user_id = Column(Integer, nullable=False)

    supply = relationship('Supplies', foreign_keys=[source_id],
                          primaryjoin=lambda: and_(Supplies.id == Expenses.source_id,
                                                   Expenses.source == "supply"))

    stage_work = relationship('StageWorks', foreign_keys=[source_id],
                              primaryjoin=lambda: and_(StageWorks.id == Expenses.source_id,
                                                         Expenses.source == "stage_work"))

    worker = relationship('Workers', foreign_keys=[source_id],
                          primaryjoin=lambda: and_(Workers.id == Expenses.source_id,
                                                   Expenses.source == "worker"))

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Expenses.user_id))
