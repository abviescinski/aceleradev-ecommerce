from pydantic import BaseModel
from enum import Enum
from typing import List, Optional
from app.api.address.schemas import ShowAddressSchema
from app.api.payment_method.schemas import ShowPaymentMethodSchema


class OrderStatus(str, Enum):
    ORDER_PLACED = 'ORDER PLACED'
    ORDER_PAID = 'ORDED PAID'
    ORDER_SHIPPED = 'ORDER SHIPPED'
    ORDER_RECEIVED = 'ORDER RECEIVED'
    ORDER_COMPLETED = 'ORDER COMPLETED'
    ORDER_CANCELLED = 'ORDER CANCELLED'


class OrderStatusesSchema(BaseModel):
    status: OrderStatus
    order_id: int


class OrderProductSchema(BaseModel):
    quantity: int
    product_id: int


class OrderSchema(BaseModel):
    address_id: int
    payment_method_id: int
    coupon_code: Optional[str] = None
    products: List[OrderProductSchema]


class ShowOrderSchema(OrderSchema):
    address: ShowAddressSchema
    payment_method: ShowPaymentMethodSchema

    class Config:
        orm_mode = True
