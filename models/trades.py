from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import and_
from db import Base
from sqlalchemy import Column, Integer, Numeric, Date, Boolean
from models.cells import Cells
from models.customers import Customers
from models.users import Users


class Trades(Base):
    __tablename__ = 'trades'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cell_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    customer_id = Column(Integer, nullable=False)
    date = Column(Date, default=datetime.today(), nullable=False)
    user_id = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False)
    discount = Column(Numeric, nullable=True)

    cell = relationship('Cells', foreign_keys=[cell_id],
                        primaryjoin=lambda: and_(Cells.id == Trades.cell_id))

    customer = relationship('Customers', foreign_keys=[customer_id],
                            primaryjoin=lambda: and_(Customers.id == Trades.customer_id))

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Trades.user_id))



