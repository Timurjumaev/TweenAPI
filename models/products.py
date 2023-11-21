from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import Column, String, Integer, and_, Numeric
from models.products_categories import ProductsCategories


class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    size = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    colour = Column(String(255), nullable=False)
    amount = Column(Integer, nullable=False)
    comment = Column(String(255), nullable=True)
    products_category_id = Column(Integer, nullable=False)
    price1 = Column(Numeric, nullable=False)
    price2 = Column(Numeric, nullable=False)
    price3 = Column(Numeric, nullable=False)

    products_category = relationship('ProductsCategories', foreign_keys=[products_category_id],
                                     primaryjoin=lambda: and_(ProductsCategories.id == Products.products_category_id))

