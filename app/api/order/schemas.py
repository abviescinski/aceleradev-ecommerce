from datetime import datetime
from pydantic import BaseModel
from enum import Enum

from app.api.customer.schemas import ShowCustomerSchema
from app.api.address.schemas import ShowAddressSchema
from app.api.payment_method.schemas import ShowPaymentMethodSchema

class OrderStatus(str, Enum):
    ORDER_PLACED = 'order_placed'
    ORDER_PAID = 'order_paid'
    ORDER_SHIPPED = 'order_shipped'
    ORDER_RECEIVED = 'order_received'
    ORDER_COMPLETED = 'order_completed'
    ORDER_CANCELLED = 'order_cancelled'

class OrderSchema(BaseModel):
    number: str
    status: OrderStatus
    create_at: datetime
    total_value: float
    total_discount: float
    customer_id: int
    address_id: int
    payment_method_id: int


class ShowOrderSchema(OrderSchema):
    customer: ShowCustomerSchema
    address: ShowAddressSchema
    payment_method: ShowPaymentMethodSchema

    class Config:
        orm_mode = True


#------------------------------------------------------------

class OrderStatusesSchema(BaseModel):
    status:OrderStatus
    create_at: datetime
    order_id: int


class OrderProductSchema(BaseModel):
    quantity:int
    order_id:int
    product:int

