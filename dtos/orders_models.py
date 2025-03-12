from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OrderCreateModel(BaseModel):
    address: str


class ProductModel(BaseModel):
    id: int
    name: str
    description: str
    price: float
    productUrl: str
    stockQuantity: int
    categoryId: int
    discount: float
    isAvailable: bool
    createdAt: datetime
    updatedAt: Optional[datetime]


class OrderDetailModel(BaseModel):
    productId: int
    price: float
    productName: str
    quantity: int
    currentPrice: float
    orderId: int
    discount: float
    createdAt: datetime
    updatedAt: Optional[datetime]
    product: ProductModel


class OrderModel(BaseModel):
    orderId: int
    userId: int
    status: bool
    orderStatus: str
    shippingAddress: str
    totalAmount: float
    paymentStatus: str
    createdAt: datetime
    updatedAt: Optional[datetime]

    class Config:
        from_attributes = True
