import pytest
import factory
from fastapi.testclient import TestClient
from requests.sessions import requote_uri
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.type_api import Emulated
from app.db.db import get_db
from app.models.models import Base
from app.app import app
from app.models.models import Base, Category, Supplier, User


@pytest.fixture()
def db_session():
    engine = create_engine('sqlite:///./test.db',
                           connect_args={'check_same_thread': False})
    Session = sessionmaker(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    yield Session()


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
def user_factory(db_session):
    class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = User
            sqlalchemy_session = db_session

        id = None
        display_name = factory.Faker('name')
        email = factory.Faker('email')
        role = None
        password = '$2b$12$FFf8bbgLa8O1ycQY6UWa2eW9G7HEXVawjm/CLJ2nZQVRvrAYwpjH6'

    return UserFactory


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
def user_admin_token(user_factory):
    user_factory(role='admin')

    return 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjcxMDQ2ODc4fQ.FqnKsA5oiiYZRMSRWur5rmWBDzdBN7K9csFdbN-Q6g8'

@pytest.fixture()
def admin_auth_header(user_admin_token):
    return {'Authorization': f'Bearer {user_admin_token}'}