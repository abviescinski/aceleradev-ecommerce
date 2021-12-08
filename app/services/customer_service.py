import bcrypt
from fastapi import Depends, HTTPException, status
from app.api.customer.schemas import CustomerSchema

from app.repositories.customer_repository import CustomerRepository
from app.repositories.user_repository import UserRepository
from app.models.models import User, Customer


class CustomerService:
    def __init__(self, customer_repository: CustomerRepository = Depends(),
                 user_repository: UserRepository = Depends()):
        self.customer_repository = customer_repository
        self.user_repository = user_repository

    def create_customer(self, customer: CustomerSchema):
        if self.user_repository.find_by_email(customer.user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already on use.")
        customer.user.password = bcrypt.hashpw(
            customer.user.password.encode('utf8'), bcrypt.gensalt())
        user_data = customer.user.dict()
        user_data.update({'role': 'customer'})
        user_data.update({'display_name': customer.first_name})
        user = self.user_repository.create(User(**user_data))
        # cria o custumer
        customer_data = customer.dict()
        customer_data.pop('user')
        customer_data.update({'user_id': user.id})
        self.customer_repository.create(Customer(**customer_data))

    def update_customer(self, id: int, customer: CustomerSchema):
        customer_data = self.customer_repository.get_by_id(id=id)
        user = self.user_repository.get_by_id(customer_data.user_id)
        if not customer_data or not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='not found.')

        query = self.user_repository.find_by_email(customer.user.email)
        if query.id != customer_data.user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already on use")
        customer.user.password = bcrypt.hashpw(
            customer.user.password.encode('utf8'), bcrypt.gensalt())
        user_data = customer.user.dict()
        user_data.update({'display_name': customer.first_name})
        self.user_repository.update(user.id, user_data)

        customer_data_update = customer.dict()
        customer_data_update.pop('user')
        customer_data_update.update({'user_id': user.id})
        self.customer_repository.update(id, customer_data_update)
