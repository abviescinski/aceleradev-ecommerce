from datetime import date, datetime
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from app.db.db import get_db
from app.models.models import OrderStatuses
from .base_repository import BaseRepository


class OrderStatusesRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(session, OrderStatuses)
        self.session = session

    def create(self, model: OrderStatuses):
        model.create_at = datetime.now()
        return super().create(model)