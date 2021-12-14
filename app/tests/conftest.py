from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.db import get_db
from app.models.models import Base
from app.app import app
import pytest


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
