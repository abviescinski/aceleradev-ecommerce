from typing import List
from fastapi import APIRouter,Depends, status

from app.api.order.schemas import OrderSchema, ShowOrderSchema, OrderStatusesSchema
from app.services.order_service import OrderService
from app.repositories.order_repository import OrderRepository

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(order: OrderSchema, service: OrderService = Depends()):
    service.create_order(order)

@router.get('/', response_model=List[ShowOrderSchema])
def index(repository: OrderRepository = Depends()):
    return repository.get_all()

@router.get('/{id}', response_model=ShowOrderSchema)
def show(id: int ,repository: OrderRepository = Depends()):
    return repository.get_by_id(id)

@router.patch('/{id}')
def update(id: int, order_status: OrderStatusesSchema, service: OrderService = Depends()):
    service.update_order(id,order_status)