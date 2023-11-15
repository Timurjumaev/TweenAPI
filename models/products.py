from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, String, Integer, and_

from models.collections import Collections


class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    size = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=True)
    collection_id = Column(Integer, nullable=False)

    collection = relationship('Collections', foreign_keys=[collection_id],
                              primaryjoin=lambda: and_(Collections.id == Products.collection_id))
