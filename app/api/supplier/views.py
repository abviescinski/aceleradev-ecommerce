from typing import List
from fastapi import APIRouter, status
from fastapi import Depends
from app.models.models import Supplier
from app.repositories.supplier_repository import SupplierRepository
from .schemas import SupplierSchema, ShowSupplierSchema
from app.services.auth_service import only_admin

#router = APIRouter(dependencies=[Depends(only_admin)])
router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ShowSupplierSchema)
def create(supplier: SupplierSchema, repository: SupplierRepository = Depends()):
    return repository.create(Supplier(**supplier.dict()))


@router.get('/', response_model=List[ShowSupplierSchema])
def index(repository: SupplierRepository = Depends()):
    return repository.get_all()


@router.put('/{id}', response_model=ShowSupplierSchema)
def update(id: int, supplier: SupplierSchema, repository: SupplierRepository = Depends()):
    return repository.update(id, supplier.dict())


@router.get('/{id}', response_model=ShowSupplierSchema)
def show(id: int, repository: SupplierRepository = Depends()):
    return repository.get_by_id(id=id)
