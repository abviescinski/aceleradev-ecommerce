from datetime import datetime
from typing import List
from fastapi import Depends, HTTPException, status
from random import randint
from app.api.order.schemas import OrderSchema, OrderStatusesSchema, OrderProductSchema
from app.models.models import Order, OrderStatuses
from app.repositories.order_repository import OrderRepository

from app.repositories.product_repository import ProductRepository
from app.repositories.coupons_repository import CouponRepository
from app.repositories.payment_method_repository import PaymentMethodRepository
from app.repositories.address_repository import AddressRepository
from app.repositories.product_discount_repository import ProductDiscountRepository
from app.repositories.order_statuses_repository import OrderStatusesRepository


class OrderService:
    def __init__(self, order_repository: OrderRepository = Depends(),
                 products_repository: ProductRepository = Depends(),
                 coupon_repository: CouponRepository = Depends(),
                 payment_method_repository: PaymentMethodRepository = Depends(),
                 address_repository: AddressRepository = Depends(),
                 product_discount_repository: ProductDiscountRepository = Depends(),
                 order_statuses_repository: OrderStatusesRepository = Depends()
                 ):
        self.order_repository = order_repository
        self.products_repository = products_repository
        self.coupon_repository = coupon_repository
        self.payment_method_repository = payment_method_repository
        self.address_repository = address_repository
        self.product_discount_repository = product_discount_repository
        self.order_statuses_repository = order_statuses_repository

        self.order = Order()
        self.order_status = OrderStatuses()

    def create_order(self, order: OrderSchema, customer_id: int):
        self.validation_order(order_view=order)
        discount = None
        #TODO: verificar quando nao tem nenhuma forma de desconto
        if order.coupon_code:
            discount = self.validation_coupon(order.coupon_code)
        else:
            discount = self.validation_discount_payment_method(
                order.products, order.payment_method_id)
        self.order.number = self.get_random()
        self.order.status = "ORDER PLACED"
        self.order.create_at = datetime.now()
        self.order.total_value = self.get_value_order(order.products)
        self.order.total_discount = self.get_total_discount(discount)
        self.order.customer_id = customer_id
        self.order.address_id = order.address_id
        self.order.payment_method_id = order.payment_method_id
        order__ = self.order_repository.create(self.order)
        # TODO: descontar produtos comprados e cupom utilizado
        #TODO: não to usando a tabela order_products
        self.generate_order_status(order__.id, "ORDER PLACED")
        self.order_statuses_repository.create(self.order_status)

    def create_status_order(self, id: int, order_status: OrderStatusesSchema):
        #TODO: o campo status da order não tá sendo alterado
        #TODO: o campo create at em order_statuses não tá com dados
        self.order_statuses_repository.create(
            OrderStatuses(**order_status.dict()))

# ------------------------------------------------------------------------------------
    def validation_order(self, order_view: OrderSchema):
        if order_view.coupon_code and not self.coupon_repository.get_by_code(order_view.coupon_code) or \
            not self.payment_method_repository.get_by_id(id=order_view.payment_method_id) or \
                not self.address_repository.get_by_id(id=order_view.address_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Informations not found.')

    def validation_coupon(self, coupon_code: str):
        coupon = self.coupon_repository.get_by_code(coupon_code)
        if not coupon.limit or coupon.expire_at < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Coupon Invalid.')
        return coupon

    def validation_discount_payment_method(self, products_list: List[OrderProductSchema], payment_method_id: int):
        ids = [product.product_id for product in products_list]
        if len(set(ids)) > 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='cart did not meet the rules for discount')
        return self.product_discount_repository.get_payment_product(payment_method_id, products_list[0].product_id)

    def get_random(self) -> int:
        cont = 0
        limit = 9999999999
        while cont <= limit:
            number = randint(1, limit)
            if not self.order_repository.check_number(str(number)):
                return number
            cont += 1
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Not order numbers available.')

    def get_value_order(self,  products_list: List[OrderProductSchema]):
        value = 0
        for product in products_list:
            query = self.products_repository.get_by_id(product.product_id)
            print("query: ", query)
            if not query:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.')

            value += query.price * product.quantity
        return value

    def get_total_discount(self, discount):
        if discount.mode == 'value':
            return discount.value
        elif discount.mode == 'percentage':
            return float(self.order.total_value)*(discount.value/100)

    def generate_order_status(self, order_id: int, status: str):
        self.order_status.order_id = order_id
        self.order_status.status = status
        self.order_status.create_at = datetime.now()

        return self.order_status

    # TODO: implementar verificação se o endereço é o mesmo do customer
