from typing import List
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session, query

from app.api.category.schemas import CategorySchema, ShowCategorySchema
from app.api.product.schemas import ProductSchema
from app.db.db import get_db
from app.models.models import Category

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(category: CategorySchema, db: Session = Depends(get_db)):
    db.add(Category(**category.dict()))
    db.commit()


@router.get('/', response_model=List[ShowCategorySchema])
def index(db: Session = Depends(get_db)):
    return db.query(Category).all()


@router.put('/{id}')
def update(id: int, product: ProductSchema, db: Session = Depends(get_db)):
    query = db.query(Category).filter_by(id=id)
    query.update(product.dict())
    db.commit()


@router.get('/{id}', response_model=ShowCategorySchema)
def show(id: int, db: Session = Depends(get_db)):
    return db.query(Category).filter_by(id=id).first()
