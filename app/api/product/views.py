from typing import List
from fastapi import APIRouter, status, Depends

from app.models.models import Product
from app.repositories.product_repository import ProductRepository
from app.services.auth_service import only_admin
from .schemas import ProductSchema, ShowProductSchema

router = APIRouter(dependencies=[Depends(only_admin)])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ShowProductSchema)
def create(product: ProductSchema, repository: ProductRepository = Depends()):
    return repository.create(Product(**product.dict()))


@router.get('/', response_model=List[ShowProductSchema])
def index(repository: ProductRepository = Depends()):
    return repository.get_all()


@router.put('/{id}')
def update(id: int, product: ProductSchema, repository: ProductRepository = Depends()):
    repository.update(id, product.dict())


@router.get('/{id}', response_model=ShowProductSchema)
def show(id: int, repository: ProductRepository = Depends()):
    return repository.get_by_id(id=id)
