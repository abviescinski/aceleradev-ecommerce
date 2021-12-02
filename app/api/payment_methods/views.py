from typing import List
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session, query

from app.api.payment_methods.schemas import PaymentMethodsSchema, ShowPaymentMethodsSchema
from app.db.db import get_db
from app.models.models import PaymentMethods

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(payment_method: PaymentMethodsSchema, db: Session = Depends(get_db)):
    db.add(PaymentMethods(**payment_method.dict()))
    db.commit()


@router.get('/', response_model=List[ShowPaymentMethodsSchema])
def index(db: Session = Depends(get_db)):
    return db.query(PaymentMethods).all()


@router.put('/{id}')
def update(id: int, payment_method: PaymentMethods, db: Session = Depends(get_db)):
    query = db.query(PaymentMethods).filter_by(id=id)
    query.update(payment_method.dict())
    db.commit()


@router.get('/{id}', response_model=ShowPaymentMethodsSchema)
def show(id:int, db: Session = Depends(get_db)):
    return db.query(PaymentMethods).filter_by(id=id).first()