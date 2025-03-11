from fastapi import APIRouter, Depends, HTTPException
from controllers.product_controller import ProductController
from dtos.auth_models import UserModel
from dtos.products_models import (
    CreateProductModel,
    ProductListModel,
    ProductModel,
    UpdateProductModel,
    ProductResponseModel,
)
from helper.token_helper import TokenHelper
from models.products_table import Product
from typing import Annotated, List, Optional

product = APIRouter(tags=["Products"])

user_dependency = Annotated[UserModel, Depends(TokenHelper.get_current_user)]


@product.post("/products/", status_code=201)
async def create_product(product: CreateProductModel, user: user_dependency):
    return ProductController.create_product(product, user)


@product.get("/products/{product_id}", response_model=ProductResponseModel)
async def read_product_by_id(product_id: int):
    return ProductController.read_product_by_id(product_id)


@product.put("/products/{product_id}")
async def update_product(
    product_id: int, product: UpdateProductModel, user: user_dependency
):
    return ProductController.update_product(product_id, product, user)


@product.delete("/products/{product_id}")
async def delete_product(product_id: int, user: user_dependency):
    return ProductController.delete_product(product_id, user)


@product.get("/products/", response_model=List[ProductListModel])
async def list_products(
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    rating: Optional[float] = None,
    discount: Optional[int] = None,
    category: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None,
):
    return ProductController.read_product(
        price_min=price_min,
        price_max=price_max,
        rating=rating,
        discount=discount,
        category=category,
        sort_by=sort_by,
        sort_order=sort_order,
    )
