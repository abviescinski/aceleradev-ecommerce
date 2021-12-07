from pydantic import BaseModel
from app.api.customer.schemas import ShowCustomerSchema


class AddressSchema(BaseModel):
    address: str
    city: str
    state: str
    number: str
    zipcode: str
    neighbourhood: str
    primary: bool
    customer_id: int


class ShowAddressSchema(AddressSchema):
    customer: ShowCustomerSchema

    class Config:
        orm_mode = True
