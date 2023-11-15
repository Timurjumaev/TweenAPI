from db import Base
from sqlalchemy import Column, String, Integer


class MaterialCategories(Base):
    __tablename__ = 'material_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=True)