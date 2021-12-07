from datetime import date
from pydantic import BaseModel


class CustomerSchema(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    genre: str
    cpf_cnpj: str
    birth_date: date


class CustomerSchemaUpdate(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    genre: str
    birth_date: date


class ShowCustomerSchema(CustomerSchema):

    class Config:
        orm_mode = True
