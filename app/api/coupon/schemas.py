from pydantic import BaseModel
from enum import Enum

from datetime import datetime


class CouponMode(str, Enum):
    value = 'value'
    percentage = 'percentage'


class CouponSchema(BaseModel):
    mode: CouponMode
    code: str
    expire_at: datetime
    limit: int
    value: float


class CouponSchemaUpdate(BaseModel):
    expire_at: datetime
    limit: int


class ShowCouponSchema(CouponSchema):

    class Config:
        orm = True
