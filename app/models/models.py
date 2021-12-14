from os import name
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import mode
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql import func
from app.db.db import Base
from sqlalchemy.sql.sqltypes import Boolean, Date, DateTime, Integer, Float, String


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45))


class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45))


class PaymentMethod(Base):
    __tablename__ = 'payment_method'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45))
    enabled = Column(Boolean, default=True)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(150))
    price = Column(Float(10, 2))
    technical_details = Column(String(255))
    image = Column(String(255))
    visible = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Category)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    supplier = relationship(Supplier)
    created_at = Column(DateTime)

    # para mostrar informações do objeto
    def __repr__(self) -> str:
        return f'description: {self.description}, price: {self.price}'


class ProductDiscount(Base):
    __tablename__ = 'product_discount'

    id = Column(Integer, primary_key=True, autoincrement=True)
    mode = Column(String(45))
    value = Column(Float)
    product_id = Column(Integer, ForeignKey('products.id'))
    products = relationship(Product)
    payment_method_id = Column(Integer, ForeignKey('payment_method.id'))
    payment_method = relationship(PaymentMethod)

    # para mostrar informações do objeto
    def __repr__(self) -> str:
        return f'value: {self.value}'


class Coupon(Base):
    __tablename__ = 'coupon'

    id = Column(Integer, primary_key=True, autoincrement=True)
    mode = Column(String(45))
    code = Column(String(10))
    expire_at = Column(DateTime)
    limit = Column(Integer)
    value = Column(Float)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    display_name = Column(String(100))
    email = Column(String(50))
    role = Column(String(10))
    password = Column(String(100))

    # para mostrar informações do objeto
    def __repr__(self) -> str:
        return f'id: {self.id}, email: {self.email}'


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(45))
    last_name = Column(String(45))
    phone_number = Column(String(45))
    genre = Column(String(45))
    cpf_cnpj = Column(String(45))
    birth_date = Column(Date)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # para mostrar informações do objeto
    def __repr__(self) -> str:
        return f'id: {self.id}, user_id: {self.user_id}, first_name: {self.first_name}'


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String)
    city = Column(String(45))
    state = Column(String(2))
    number = Column(String(10))
    zipcode = Column(String(6))
    neighbourhood = Column(String(45))
    primary = Column(Boolean)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customer = relationship(Customer)


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(10))
    status = Column(String(15))
    create_at = Column(DateTime)
    total_value = Column(Float)
    total_discount = Column(Float)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customer = relationship(Customer)
    address_id = Column(Integer, ForeignKey('address.id'))
    address = relationship(Address)
    payment_method_id = Column(Integer, ForeignKey('payment_method.id'))
    payment_method = relationship(PaymentMethod)

    # para mostrar informações do objeto
    def __repr__(self) -> str:
        return f'id: {self.id}, number: {self.number}'




class OrderStatuses(Base):
    __tablename__ = 'order_statuses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(15))
    create_at = Column(DateTime)
    order_id = Column(Integer, ForeignKey('order.id'))
    order = relationship(Order)


class OrderProducts(Base):
    __tablename__ = 'order_products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer)
    order_id = Column(Integer, ForeignKey('order.id'))
    order = relationship(Order)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship(Product)
