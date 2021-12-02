from pydantic import BaseModel
from app.api.supplier.schemas import ShowSupplierSchema
from app.api.category.schemas import ShowCategorySchema

from app.models.models import Category


class ProductSchema(BaseModel):
    description: str
    price: float
    technical_details: str
    image: str
    visible: bool
    category_id: int
    supplier_id: int


class ShowProductSchema(ProductSchema):
    id: int
    category: ShowCategorySchema
    supplier: ShowSupplierSchema

    class Config:
        orm_mode = True
