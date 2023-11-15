from db import Base
from sqlalchemy import Column, String, Integer


class ProductsCategories(Base):
    __tablename__ = 'products_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=True)
