from sqlalchemy.orm import relationship, backref
from db import Base
from sqlalchemy import Column, Integer, String, and_

from models.customers import Customers
from models.suppliers import Suppliers
from models.users import Users
from models.workers import Workers


class Phones(Base):
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, nullable=False)
    source = Column(String(255), nullable=False)
    source_id = Column(Integer, nullable=False)
    comment = Column(String(255), nullable=False)

    user = relationship('Users', foreign_keys=[source_id],
                        primaryjoin=lambda: and_(Users.id == Phones.source_id, Phones.source == "user"),
                        backref=backref("phones"))

    worker = relationship('Workers', foreign_keys=[source_id],
                          primaryjoin=lambda: and_(Workers.id == Phones.source_id, Phones.source == "worker"),
                          backref=backref("phones"))

    supplier = relationship('Suppliers', foreign_keys=[source_id],
                            primaryjoin=lambda: and_(Suppliers.id == Phones.source_id, Phones.source == "supplier"),
                            backref=backref("phones"))

    customer = relationship('Customers', foreign_keys=[source_id],
                            primaryjoin=lambda: and_(Customers.id == Phones.source_id, Phones.source == "customer"),
                            backref=backref("phones"))
