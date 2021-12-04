from pydantic import BaseModel
from enum import Enum
from app.api.product.schemas import ShowProductSchema
from app.api.payment_methods.schemas import ShowPaymentMethodsSchema


class DiscountMode(str, Enum):
    value = 'value'
    percentage = 'percentage'


class ProductsDiscountsSchema(BaseModel):
    mode: DiscountMode
    value: float
    product_id: int
    payment_methods_id: int


class ShowProductsDiscountsSchema(ProductsDiscountsSchema):
    id: int
    product: ShowProductSchema
    payment_methods: ShowPaymentMethodsSchema

    class Config:
        orm_mode = True
