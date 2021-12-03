from typing import List
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.api.products_discounts.schemas import ProductsDiscountsSchema, ShowProductsDiscountsSchema
from app.models.models import ProductDiscounts
from app.db.db import get_db

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(products_discounts: ProductsDiscountsSchema, db: Session = Depends(get_db)):
    db.add(ProductDiscounts(**products_discounts.dict()))
    db.commit()    


@router.get('/')
def index(db: Session = Depends(get_db)):
    return db.query(ProductDiscounts).all()


@router.put('/{id}')
def update(id: int, products_discounts: ProductsDiscountsSchema,db: Session = Depends(get_db)):
    query = db.query(ProductDiscounts).filter_by(id=id)
    query.update(products_discounts.dict())
    db.commit()


#TODO: desse jeito da linha 31 não funciona, perguntar ao professor.
#@router.get('/{id}', response_model=ShowProductsDiscountsSchema)
@router.get('/{id}')
def show(id: int, db: Session = Depends(get_db)):
    return db.query(ProductDiscounts).filter_by(id=id).first()
