from datetime import datetime
from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import Column, String, Integer, Numeric, Date, Boolean, and_

from models.cells import Cells
from models.products import Products
from models.users import Users
from models.stages import Stages
from models.customers import Customers


class Works(Base):
    __tablename__ = 'works'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(255), nullable=False)
    product_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    comment = Column(String(999), nullable=False)
    date = Column(Date, default=datetime.today(), nullable=False)
    user_id = Column(Integer, nullable=False)
    stage_id = Column(Integer, nullable=False)
    stage_status = Column(Boolean, default=False, nullable=False)
    status = Column(Boolean, default=False, nullable=False)
    price = Column(Numeric, nullable=True)
    customer_id = Column(Integer, nullable=True)
    finish_date = Column(Date, nullable=True)
    cell_id = Column(Integer, nullable=True)

    product = relationship('Products', foreign_keys=[product_id],
                           primaryjoin=lambda: and_(Products.id == Works.product_id))

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Works.user_id))

    stage = relationship('Stages', foreign_keys=[stage_id],
                         primaryjoin=lambda: and_(Stages.id == Works.stage_id))

    customer = relationship('Customers', foreign_keys=[customer_id],
                            primaryjoin=lambda: and_(Customers.id == Works.customer_id))

    cell = relationship('Cells', foreign_keys=[cell_id],
                        primaryjoin=lambda: and_(Cells.id == Works.cell_id))

