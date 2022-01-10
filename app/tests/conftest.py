import datetime
import pytest
import factory
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.db import get_db
from app.models.models import Base, Address, Coupon, Customer, Order, PaymentMethod, Product, ProductDiscount, Category, Supplier, User
from app.app import app
from datetime import datetime, timedelta


@pytest.fixture()
def db_session():
    engine = create_engine('sqlite:///./test.db',
                           connect_args={'check_same_thread': False})
    Session = sessionmaker(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db = Session()
    yield db
    db.close()


@pytest.fixture()
def override_get_db(db_session):
    def _override_get_db():
        yield db_session

    return _override_get_db


@pytest.fixture()
def client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    return client


@pytest.fixture()
def category_factory(db_session):
    class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Category
            sqlalchemy_session = db_session

        id = factory.Faker('pyint')
        name = factory.Faker('name')

    return CategoryFactory


@pytest.fixture()
def supplier_factory(db_session):
    class SupplierFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Supplier
            sqlalchemy_session = db_session

        id = factory.Faker('pyint')
        name = factory.Faker('name')

    return SupplierFactory


@pytest.fixture()
def user_factory(db_session):
    class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = User
            sqlalchemy_session = db_session

        id = None
        display_name = factory.Faker('name')
        email = factory.Faker('email')
        role = factory.Faker('word')
        password = '$2b$12$FFf8bbgLa8O1ycQY6UWa2eW9G7HEXVawjm/CLJ2nZQVRvrAYwpjH6'

    return UserFactory


@pytest.fixture()
def user_admin_token(user_factory):
    user_factory(role='admin')

    return 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjcxMDQ2ODc4fQ.FqnKsA5oiiYZRMSRWur5rmWBDzdBN7K9csFdbN-Q6g8'


@pytest.fixture()
def admin_auth_header(user_admin_token):
    return {'Authorization': f'Bearer {user_admin_token}'}


@pytest.fixture()
def user_customer_token(user_factory):
    user_factory(id=2, email='cliente1@email', role='customer', password='$2b$12$YuYlGDv6Hid0pSwzLALyU.N/od4Lp28tXSoR9rbxvx9cNJesNNqtq')

    return 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZXhwIjoxNjcxMjAwMTQ0fQ.tYpFXtY8jtNj5dw-ayxSF4zZkUs3U6H2OrNySTSrYNA'


@pytest.fixture()
def customer_auth_header(user_customer_token):
    return {'Authorization': f'Bearer {user_customer_token}'}


@pytest.fixture()
def product_factory(db_session, category_factory, supplier_factory):
    class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Product
            sqlalchemy_session = db_session

        id = factory.Faker('pyint')
        description = factory.Faker('word')
        price = factory.Faker('pyfloat')
        technical_details = factory.Faker('word')
        image = factory.Faker('word')
        visible = True
        category = factory.SubFactory(category_factory)
        supplier = factory.SubFactory(supplier_factory)

    return ProductFactory


@pytest.fixture()
def customer_factory(db_session, user_factory):
    class CustomerFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Customer
            sqlalchemy_session = db_session

        id = factory.Sequence(int)
        first_name = factory.Faker('first_name')
        last_name = factory.Faker('last_name')
        phone_number = factory.Faker('phone_number')
        genre = factory.Faker('word')
        cpf_cnpj = factory.Faker('pyint')
        birth_date = factory.Faker('date_time')
        user = factory.SubFactory(user_factory)

    return CustomerFactory


@pytest.fixture()
def address_factory(db_session, customer_factory):
    class AddressFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Address
            sqlalchemy_session = db_session

        id = factory.Sequence(int)
        address = factory.Faker('street_name')
        city = factory.Faker('city')
        state = factory.Faker('country_code')
        number = factory.Faker('building_number')
        zipcode = factory.Faker('postcode')
        neighbourhood = factory.Faker('street_name')
        primary = True
        customer = factory.SubFactory(customer_factory)

    return AddressFactory


@pytest.fixture()
def coupon_factory(db_session):
    class CouponFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Coupon
            sqlalchemy_session = db_session

        id = factory.Sequence(int)
        mode = 'value'
        code = factory.Faker('pyint')
        expire_at = datetime.now()+timedelta(days=10)
        limit = factory.Faker('pyint')

    return CouponFactory


@pytest.fixture()
def payment_method_factory(db_session):
    class PaymentMethodFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = PaymentMethod
            sqlalchemy_session = db_session

        id = factory.Sequence(int)
        name = factory.Faker('credit_card_provider')
        enabled = True

    return PaymentMethodFactory


@pytest.fixture()
def product_discount_factory(db_session, product_factory, payment_method_factory):
    class ProductDiscountFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = ProductDiscount
            sqlalchemy_session = db_session

        id = factory.Sequence(int)
        mode = 'value'
        value = 10
        product = factory.SubFactory(product_factory)
        payment_method = factory.SubFactory(payment_method_factory)

    return ProductDiscountFactory


@pytest.fixture()
def order_factory(db_session, customer_factory, address_factory, payment_method_factory):
    class OrderFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Order
            sqlalchemy_session = db_session

        id = factory.Sequence(int)
        number = factory.Faker('pyint')
        status = 'ORDER PLACED'
        create_at = factory.Faker('date_time')
        total_value = None
        total_discount = None
        customer = factory.SubFactory(customer_factory)
        address = factory.SubFactory(address_factory)
        payment_method = factory.SubFactory(payment_method_factory)

    return OrderFactory
