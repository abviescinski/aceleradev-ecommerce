
from fastapi import Depends, HTTPException, status
from app.api.coupon.schemas import CouponSchema
from app.models.models import Coupon
from app.repositories.coupons_repository import CouponRepository

class CouponService:
    def __init__(self, coupon_repository: CouponRepository = Depends()):
        self.coupon_repository = coupon_repository


    def create_coupon(self, coupon: CouponSchema):
        if coupon.code is None or coupon.code == 'string':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Coupon Code Invalid.')
        if self.coupon_repository.is_duplicate(coupon_code=coupon.code):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Coupon Code Already Exists')
        self.coupon_repository.create(Coupon(**coupon.dict()))