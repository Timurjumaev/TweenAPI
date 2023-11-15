from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import Column, Integer, Numeric, and_
from models.materials import Materials


class WarehouseMaterials(Base):
    __tablename__ = 'warehouse_materials'
    id = Column(Integer, primary_key=True, autoincrement=True)
    material_id = Column(Integer, nullable=False)
    amount = Column(Numeric, nullable=False)
    price = Column(Numeric, nullable=False)

    material = relationship('Materials', foreign_keys=[material_id],
                            primaryjoin=lambda: and_(Materials.id == WarehouseMaterials.material_id))
