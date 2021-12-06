from typing import List
from fastapi import APIRouter, status, Depends
from app.models.models import Coupon

from app.repositories.coupons_repository import CouponRepository
from app.services.coupons_service import CouponService

from .schemas import CouponSchema, CouponSchemaUpdate, ShowCouponSchema


router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(coupon: CouponSchema, service: CouponService = Depends()):
    service.create_coupon(coupon)

#TODO: idem
# @router.get('/', response_model=List[ShowCouponSchema])


@router.get('/')
def index(repository: CouponRepository = Depends()):
    return repository.get_all()


@router.put('/{id}')
def update(id: int, coupon: CouponSchemaUpdate, repository: CouponRepository = Depends()):
    repository.update(id, coupon.dict())


@router.get('/{id}')
def show(id: int, repository: CouponRepository = Depends()):
    return repository.get_by_id(id=id)


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete(id: int, repository: CouponRepository = Depends()):
    repository.delete(id=id)
