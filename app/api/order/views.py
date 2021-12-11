from typing import List
from fastapi import APIRouter,Depends, status

from app.api.order.schemas import OrderSchema, ShowOrderSchema, OrderStatusesSchema
from app.models.models import Customer
from app.services.auth_service import get_user, only_customer, only_admin
from app.services.order_service import OrderService
from app.repositories.order_repository import OrderRepository

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, dependencies=[Depends(only_customer)])
def create(order: OrderSchema, service: OrderService = Depends(), customer: Customer = Depends(get_user)):
    service.create_order(order, customer.id)

#@router.get('/', response_model=List[ShowOrderSchema]) #TODO: quando deixa assim dá erro de typing
@router.get('/')
def index(repository: OrderRepository = Depends()):
    return repository.get_all()

#@router.get('/{id}', response_model=ShowOrderSchema)
@router.get('/{id}')
def show(id: int ,repository: OrderRepository = Depends()):
    return repository.get_by_id(id)

@router.patch('/{id}', dependencies=[Depends(only_admin)])
def update(order_id: int, order_status: OrderStatusesSchema, service: OrderService = Depends()):
    service.create_status_order(order_id,order_status)