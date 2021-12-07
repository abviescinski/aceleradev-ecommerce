from fastapi import APIRouter, status, Depends
from app.api.customer.schemas import CustomerSchema, CustomerSchemaUpdate, ShowCustomerSchema
from app.models.models import Customer
from app.repositories.customer_repository import CustomerRepository

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(customer: CustomerSchema, repository: CustomerRepository = Depends()):
    repository.create(Customer(**customer.dict()))


@router.get('/')
def index(repository: CustomerRepository = Depends()):
    return repository.get_all()


@router.put('/{id}')
def update(id: int, customer: CustomerSchemaUpdate, repository: CustomerRepository = Depends()):
    repository.update(id, customer.dict())


@router.get('/{id}', response_model=ShowCustomerSchema)
# @router.get('/{id}')
def show(id: int, repository: CustomerRepository = Depends()):
    return repository.get_by_id(id=id)
