from fastapi import APIRouter
from .product.views import router as product_router
from .category.views import router as category_router
from .supplier.views import router as supplier_router
from .payment_method.views import router as payment_method_router
from .product_discount.views import router as product_discount_router

router = APIRouter()

router.include_router(product_router, prefix='/product',  tags=['product'])
router.include_router(category_router, prefix='/category', tags=['category'])
router.include_router(supplier_router, prefix='/supplier', tags=['supplier'])
router.include_router(payment_method_router, prefix='/payment_method', tags=['payment_method'])
router.include_router(product_discount_router, prefix='/products_discounts', tags=['product_discount'])
