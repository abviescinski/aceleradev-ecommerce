from fastapi import APIRouter, status, Depends

from app.api.address.schemas import AddressSchema, ShowCustomerSchema
from app.repositories.address_repository import AddressRepository
from app.services.address_service import AddressService

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(address: AddressSchema, service: AddressService = Depends()):
    service.create_address(address)


@router.get('/')
def index(repository: AddressRepository = Depends()):
    return repository.get_all()


@router.put('/{id}')
def update(id: int, address: AddressSchema, service: AddressService = Depends()):
    service.update_address(id, address)


@router.get('/{id}', response_model=ShowCustomerSchema)
def show(id: int, repository: AddressRepository = Depends()):
    return repository.get_by_id(id=id)


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete(id: int, repository: AddressRepository = Depends()):
    repository.delete(id=id)
