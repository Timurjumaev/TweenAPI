from sqlalchemy.orm import relationship
from models.products_categories import ProductsCategories
from db import Base
from sqlalchemy import Column, String, Integer, and_


class Collections(Base):
    __tablename__ = 'collections'
    id = Column(Integer, primary_key=True, autoincrement=True)
    model = Column(String(255), nullable=False)
    colour = Column(String(255), nullable=False)
    amount = Column(Integer, nullable=False)
    comment = Column(String(255), nullable=True)
    products_category_id = Column(Integer, nullable=False)

    products_category = relationship('ProductsCategories', foreign_keys=[products_category_id],
                                     primaryjoin=lambda: and_(ProductsCategories.id == Collections.products_category_id))

