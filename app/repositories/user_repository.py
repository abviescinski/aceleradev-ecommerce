from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.models import User
from .base_repository import BaseRepository


class UserRespository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(session, User)
        self.session = session

    def find_by_email(self, email):
        return self.session.query(self.model).filter_by(email=email).first()