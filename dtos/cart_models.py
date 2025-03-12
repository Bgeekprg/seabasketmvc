from pydantic import BaseModel
from decimal import Decimal


class CartResponseModel(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    price: Decimal
    product_name: str

    class Config:
        from_attributes = True
