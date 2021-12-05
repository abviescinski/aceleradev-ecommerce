from fastapi.param_functions import Depends
from sqlalchemy.orm import Session

from app.db.db import get_db
from .base_repository import BaseRepository
from app.models.models import PaymentMethod


class PaymentMethodRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(session, PaymentMethod)
