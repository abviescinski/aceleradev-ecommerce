from typing import List
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session, query

from app.api.payment_method.schemas import PaymentMethodSchema, ShowPaymentMethodSchema
from app.db.db import get_db
from app.models.models import PaymentMethod
from app.repositories.payment_method_repository import PaymentMethodRepository

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(payment_method: PaymentMethodSchema, repository: PaymentMethodRepository = Depends()):
    repository.create(PaymentMethod(**payment_method.dict()))


@router.get('/', response_model=List[ShowPaymentMethodSchema])
def index(repository: PaymentMethodRepository = Depends()):
    return repository.get_all()


@router.put('/{id}')
def update(id: int, payment_method: PaymentMethodSchema, repository: PaymentMethodRepository = Depends()):
    repository.update(id, payment_method.dict())


@router.get('/{id}', response_model=ShowPaymentMethodSchema)
def show(id: int, repository: PaymentMethodRepository = Depends()):
    return repository.get_by_id(id=id)
