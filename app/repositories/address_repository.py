from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.models import Address
from .base_repository import BaseRepository


class AddressRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(session, Address)
        self.session = session

    def delete(self, id: int):
        self.session.query(self.model).filter_by(id=id).delete()
        self.session.commit()

    def remove_primary(self):
        return self.session.query(self.model).filter_by(primary=True).update({"primary": False})
