from datetime import date
from pydantic import BaseModel


class UserCustomerSchema(BaseModel):
    email: str
    password: str


class CustomerSchema(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    genre: str
    cpf_cnpj: str
    birth_date: date
    user: UserCustomerSchema


class CustomerSchemaUpdate(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    genre: str
    birth_date: date
    user: UserCustomerSchema


class ShowCustomerSchema(CustomerSchema):
    user: UserCustomerSchema

    class Config:
        orm_mode = True
