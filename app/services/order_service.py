
from fastapi import Depends, HTTPException, status
from app.api.order.schemas import OrderSchema, OrderStatusesSchema
from app.models.models import Order
from app.repositories.order_repository import OrderRepository


class OrderService:
    def __init__(self, order_repository: OrderRepository = Depends()):
        self.order_repository = order_repository

    def create_order(self, order: OrderSchema):
        ...

    def update_order(self, order_status: OrderStatusesSchema):
        ...