from fastapi import APIRouter, status, Depends
from app.api.product_discount.schemas import ProductDiscountSchema
from app.models.models import ProductDiscount
from app.repositories.product_discount_repository import ProductDiscountRepository
from app.services.product_discount_service import ProductDiscountService

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(discount: ProductDiscountSchema, service: ProductDiscountService = Depends()):
    service.create_discount(discount)


@router.get('/')
def index(repository: ProductDiscountRepository = Depends()):
    return repository.get_all()


@router.put('/{id}')
def update(id: int, discount: ProductDiscountSchema, repository: ProductDiscountRepository = Depends()):
    repository.update(id, discount.dict())


# TODO: desse jeito da linha 31 não funciona, perguntar ao professor.
# @router.get('/{id}', response_model=ShowProductsDiscountsSchema)
@router.get('/{id}')
def show(id: int, repository: ProductDiscountRepository = Depends()):
    return repository.get_by_id(id=id)


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete(id: int, repository: ProductDiscountRepository = Depends()):
    repository.delete(id=id)
