from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.models import Order
from .base_repository import BaseRepository


class OrderRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(session, Order)
        self.session = session

    def check_number(self, number: str):
        return self.session.query(self.model).filter_by(number=number).first()