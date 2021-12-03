from ast import Str
from sqlalchemy.orm import relationship

from sqlalchemy.sql.schema import ForeignKey
from app.db.db import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Boolean, Integer, Float, String


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(45))


class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True)
    name = Column(String(45))


class PaymentMethods(Base):
    __tablename__ = 'payment_methods'

    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    enabled = Column(Boolean)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    description = Column(String(150))
    price = Column(Float(10, 2))
    technical_details = Column(String(255))
    image = Column(String(255))
    visible = Column(Boolean, default=True)
    categoriy_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Category)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    supplier = relationship(Supplier)


class ProductDiscounts(Base):
    __tablename__ = 'product_discounts'

    id = Column(Integer, primary_key=True)
    mode = Column(String(45))
    value = Column(Float)
    product_id = Column(Integer, ForeignKey('products.id'))
    products = relationship(Product)
    payment_methods_id = Column(Integer, ForeignKey('payment_methods.id'))
    payment_methods = relationship(PaymentMethods)
