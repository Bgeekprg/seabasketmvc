from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
from datetime import datetime


class CreateProductModel(BaseModel):
    name: str = Field(..., min_length=1, description="The name of the product.")
    description: Optional[str] = None
    stockQuantity: int = Field(
        default=0,
        ge=0,
        description="The quantity of the product in stock, must be non-negative.",
    )
    price: Decimal = Field(
        ..., gt=0, description="The price of the product, must be greater than 0."
    )
    categoryId: Optional[int] = None
    productUrl: Optional[str] = None
    discount: Optional[int] = None
    rating: Optional[Decimal] = None
    isAvailable: bool = True


class UpdateProductModel(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, description="The name of the product."
    )
    description: Optional[str] = None
    stockQuantity: Optional[int] = Field(
        None,
        ge=0,
        description="The quantity of the product in stock, must be non-negative.",
    )
    price: Optional[Decimal] = Field(
        None, gt=0, description="The price of the product, must be greater than 0."
    )
    categoryId: Optional[int] = None
    productUrl: Optional[str] = None
    discount: Optional[int] = None
    rating: Optional[Decimal] = None
    isAvailable: Optional[bool] = None


class ProductResponseModel(BaseModel):
    id: int
    name: str
    description: Optional[str]
    stockQuantity: int
    price: Decimal
    categoryId: Optional[int]
    productUrl: Optional[str]
    discount: Optional[int]
    rating: Optional[Decimal]
    isAvailable: bool
    createdAt: datetime
    updatedAt: Optional[datetime] = None
    images: Optional[List[str]] = None



class ProductModel(BaseModel):
    id: int
    name: str = Field(..., min_length=1, description="The name of the product.")
    description: Optional[str] = None
    stockQuantity: int = Field(
        default=0,
        ge=0,
        description="The quantity of the product in stock, must be non-negative.",
    )
    price: Decimal = Field(
        ..., gt=0, description="The price of the product, must be greater than 0."
    )
    categoryId: Optional[int] = None
    productUrl: Optional[str] = None
    discount: Optional[int] = None
    rating: Optional[Decimal] = None
    isAvailable: bool = True
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]


class ProductListModel(BaseModel):
    id: int
    name: str
    stockQuantity: int
    price: Decimal
    categoryId: Optional[int]
    productUrl: Optional[str]
    discount: Optional[int]
    rating: Optional[Decimal]

    class Config:
        orm_mode = True


class ProductFilterModel(BaseModel):
    product_name: Optional[str] = Field(None, description="Product name for filtering.")
    price_min: Optional[float] = Field(None, description="Minimum price for filtering.")
    price_max: Optional[float] = Field(None, description="Maximum price for filtering.")
    rating: Optional[float] = Field(None, description="Rating for filtering.")
    discount: Optional[int] = Field(None, description="Discount for filtering.")
    category: Optional[int] = Field(None, description="Category for filtering.")
    sort_by: Optional[str] = Field(
        None, description="Field to sort by (e.g., price, name)."
    )
    sort_order: Optional[str] = Field(
        None, description="Order to sort (e.g., ascending, descending)."
    )
