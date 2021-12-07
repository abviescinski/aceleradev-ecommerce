
from fastapi import Depends, HTTPException, status
from app.models.models import Address
from app.repositories.address_repository import AddressRepository
from app.repositories.customer_repository import CustomerRepository
from app.api.address.schemas import AddressSchema


class AddressService:
    def __init__(self, address_repository: AddressRepository = Depends(), customer_repository: CustomerRepository = Depends()):
        self.address_repository = address_repository
        self.customer_repository = customer_repository

    def check(self, address: AddressSchema):
        if self.customer_repository.get_by_id(address.customer_id) in None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Customer not found.')
        if address.primary:
            self.address_repository.remove_primary()

    def create_address(self, address: AddressSchema):
        #address = self.check(address)
        if not self.customer_repository.get_by_id(address.customer_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Customer not found.')
        if address.primary:
            self.address_repository.remove_primary()
        self.address_repository.create(Address(**address.dict()))

    def update_address(self, id: int, address: AddressSchema):
        #address = self.check(address)
        if not self.customer_repository.get_by_id(address.customer_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Customer not found.')
        if address.primary:
            self.address_repository.remove_primary()
        self.address_repository.update(id=id, attributes=address.dict())
