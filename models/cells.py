from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import Column, String, Integer, Numeric, and_
from models.products import Products


class Cells(Base):
    __tablename__ = 'cells'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    price = Column(Numeric, nullable=False)
    product_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False, default=0)

    product = relationship('Products', foreign_keys=[product_id],
                           primaryjoin=lambda: and_(Products.id == Cells.product_id))
