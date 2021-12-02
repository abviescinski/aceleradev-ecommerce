from pydantic import BaseModel


class PaymentMethodsSchema(BaseModel):
    name: str
    enable: bool


class ShowPaymentMethodsSchema(PaymentMethodsSchema):
    id: int

    class Config:
        orm_mode = True