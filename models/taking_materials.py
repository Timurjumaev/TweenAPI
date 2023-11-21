from datetime import datetime
from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import Column, Integer, Numeric, Date, and_
from models.materials import Materials


class TakingMaterials(Base):
    __tablename__ = 'taking_materials'
    id = Column(Integer, primary_key=True, autoincrement=True)
    material_id = Column(Integer, nullable=False)
    amount = Column(Numeric, nullable=False)
    date = Column(Date, default=datetime.today(), nullable=False)

    material = relationship('Materials', foreign_keys=[material_id],
                            primaryjoin=lambda: and_(Materials.id == TakingMaterials.material_id))
