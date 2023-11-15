from sqlalchemy.orm import relationship, backref
from db import Base
from sqlalchemy import Column, Integer, String, and_, Text

from models.collections import Collections
from models.materials import Materials
from models.materials_categories import MaterialCategories
from models.products import Products
from models.products_categories import ProductsCategories
from models.users import Users
from models.workers import Workers


class Files(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True, autoincrement=True)
    file = Column(Text, nullable=False)
    source = Column(String(255), nullable=False)
    source_id = Column(Integer, nullable=False)

    user = relationship('Users', foreign_keys=[source_id],
                        primaryjoin=lambda: and_(Users.id == Files.source_id, Files.source == "user"),
                        backref=backref("files"))

    worker = relationship('Workers', foreign_keys=[source_id],
                          primaryjoin=lambda: and_(Workers.id == Files.source_id, Files.source == "worker"),
                          backref=backref("files"))

    material = relationship('Materials', foreign_keys=[source_id],
                            primaryjoin=lambda: and_(Materials.id == Files.source_id, Files.source == "material"),
                            backref=backref("files"))

    materials_categories = relationship('MaterialCategories', foreign_keys=[source_id],
                                        primaryjoin=lambda: and_(MaterialCategories.id == Files.source_id,
                                                                 Files.source == "materials_category"),
                                        backref=backref("files"))

    products_categories = relationship('ProductsCategories', foreign_keys=[source_id],
                                       primaryjoin=lambda: and_(ProductsCategories.id == Files.source_id,
                                                                Files.source == "products_category"),
                                       backref=backref("files"))

    collections = relationship('Collections', foreign_keys=[source_id],
                               primaryjoin=lambda: and_(Collections.id == Files.source_id,
                                                        Files.source == "collection"),
                               backref=backref("files"))

    products = relationship('Products', foreign_keys=[source_id],
                            primaryjoin=lambda: and_(Products.id == Files.source_id,
                                                     Files.source == "product"),
                            backref=backref("files"))
