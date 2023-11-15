from datetime import datetime
from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import Column, Integer, Numeric, Date, Boolean, and_

from models.materials import Materials
from models.suppliers import Suppliers
from models.users import Users


class Supplies(Base):
    __tablename__ = 'supplies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    material_id = Column(Integer, nullable=False)
    supplier_id = Column(Integer, nullable=False)
    amount = Column(Numeric, nullable=False)
    price = Column(Numeric, nullable=False)
    status = Column(Boolean, nullable=False)
    date = Column(Date, default=datetime.today(), nullable=False)
    user_id = Column(Integer, nullable=False)

    material = relationship('Materials', foreign_keys=[material_id],
                            primaryjoin=lambda: and_(Materials.id == Supplies.material_id))

    supplier = relationship('Suppliers', foreign_keys=[supplier_id],
                            primaryjoin=lambda: and_(Suppliers.id == Supplies.supplier_id))

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Supplies.user_id))
