from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
#from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base
from app.settings import settings


DB_PATH = Path(__file__).resolve().parent
#SQLALCHEMY_DATABASE_URL = f'sqlite:///{DB_PATH}/database.db'

engine = create_engine(settings.db_url, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()

metadata = Base.metadata


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
