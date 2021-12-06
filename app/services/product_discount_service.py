from fastapi import Depends, HTTPException, status
from app.repositories.payment_method_repository import PaymentMethodRepository
from app.repositories.product_discount_repository import ProductDiscountRepository
from app.api.product_discount.schemas import ProductDiscountSchema
from app.models.models import ProductDiscount


class ProductDiscountService:
    def __init__(self, payment_method_repository: PaymentMethodRepository = Depends(),
                 product_discount_repository: ProductDiscountRepository = Depends()):
        self.payment_method_repository = payment_method_repository
        self.product_discount_repository = product_discount_repository

    def create_discount(self, discount: ProductDiscountSchema):
        payment_method = self.product_discount_repository.get_payment_method_id(
            payment_method_id=discount.payment_method_id)
        if not payment_method or payment_method.enabled == False:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Payment method not found.')
        if self.product_discount_repository.get_payment_method_in_discount(payment_method_id=discount.payment_method_id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='There is already a discount for this form of payment.')
        self.payment_method_repository.create(
            ProductDiscount(**discount.dict()))
