from typing import List
from fastapi import APIRouter, status, Depends
from app.api.customer.schemas import CustomerSchema, CustomerSchemaUpdate, ShowCustomerSchema
from app.repositories.customer_repository import CustomerRepository
from app.services.customer_service import CustomerService

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(customer: CustomerSchema, service: CustomerService = Depends()):
    service.create_customer(customer)


@router.get('/')
def index(repository: CustomerRepository = Depends()):
    return repository.get_all()


@router.put('/{id}')
def update(id: int, customer: CustomerSchemaUpdate, service: CustomerService = Depends()):
    service.update_customer(id, customer)


# @router.get('/{id}', response_model=List[ShowCustomerSchema])
@router.get('/{id}')
def show(id: int, repository: CustomerRepository = Depends()):
    return repository.get_by_id(id=id)
