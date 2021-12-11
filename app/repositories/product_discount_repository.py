from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session

from app.db.db import get_db
from app.models.models import ProductDiscount, PaymentMethod
from .base_repository import BaseRepository


class ProductDiscountRepository(BaseRepository):
    def __init__(self, session: Session = Depends(get_db)):
        super().__init__(session, ProductDiscount)
        self.session = session

    def delete(self, id: int):
        self.session.query(ProductDiscount).filter_by(id=id).delete()
        self.session.commit()

    def get_payment_method_id(self, payment_method_id: int):
        return self.session.query(PaymentMethod).filter_by(
            id=payment_method_id).first()

    def get_payment_method_in_discount(self, payment_method_id: int):
        return self.session.query(self.model).filter_by(payment_method_id=payment_method_id).first()

    def get_payment_product(self,payment_method_id: int, product_id: int):
        return self.session.query(self.model).filter_by(payment_method_id=payment_method_id, product_id=product_id).first()