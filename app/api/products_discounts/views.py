from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.products_discounts.schemas import ProductsDiscountsSchema, ShowProductsDiscountsSchema
from app.models.models import PaymentMethods, ProductDiscounts
from app.db.db import get_db

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(products_discounts: ProductsDiscountsSchema, db: Session = Depends(get_db)):
    payment_method = db.query(PaymentMethods).filter_by(id=products_discounts.payment_methods_id).first()
    if not payment_method or payment_method.enabled == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Payment method not found.')
    if db.query(ProductDiscounts).filter_by(payment_methods_id=products_discounts.payment_methods_id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='There is already a discount for this form of payment.')
    db.add(ProductDiscounts(**products_discounts.dict()))
    db.commit()    


@router.get('/')
def index(db: Session = Depends(get_db)):
    return db.query(ProductDiscounts).all()


@router.put('/{id}')
def update(id: int, products_discounts: ProductsDiscountsSchema, db: Session = Depends(get_db)):
    query = db.query(ProductDiscounts).filter_by(id=id)
    query.update(products_discounts.dict())
    db.commit()


#TODO: desse jeito da linha 31 não funciona, perguntar ao professor.
#@router.get('/{id}', response_model=ShowProductsDiscountsSchema)
@router.get('/{id}')
def show(id: int, db: Session = Depends(get_db)):
    return db.query(ProductDiscounts).filter_by(id=id).first()


@router.delete('/{id}', status_code=status.HTTP_410_GONE)
def delete(id: int, db: Session = Depends(get_db)):
    db.query(ProductDiscounts).filter_by(id=id).delete()
    db.commit()