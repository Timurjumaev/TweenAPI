from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import Column, String, Integer, and_
from models.materials_categories import MaterialCategories


class Materials(Base):
    __tablename__ = 'materials'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    measure = Column(String(255), nullable=False)
    materials_category_id = Column(Integer, nullable=False)

    materials_category = relationship('MaterialCategories', foreign_keys=[materials_category_id],
                                      primaryjoin=lambda: and_(MaterialCategories.id == Materials.materials_category_id))
