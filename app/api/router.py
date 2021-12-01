from fastapi import APIRouter
from .product.views import router as product_router
from .product.views import router as category_router

router = APIRouter()

router.include_router(product_router, prefix='/product')
router.include_router(category_router, prefix='/category')
