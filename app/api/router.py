from fastapi import APIRouter
from .product.views import router as product_router
from .category.views import router as category_router
from .supplier.views import router as supplier_router
from .payment_methods.views import router as payment_methods_router
from .products_discounts.views import router as products_discounts_router

router = APIRouter()

router.include_router(product_router, prefix='/product',  tags=['product'])
router.include_router(category_router, prefix='/category', tags=['category'])
router.include_router(supplier_router, prefix='/supplier', tags=['supplier'])
router.include_router(payment_methods_router, prefix='/payment_methods', tags=['payment_methods'])
router.include_router(products_discounts_router, prefix='/products_discounts', tags=['products_discounts'])
