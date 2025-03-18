from fastapi import APIRouter, Depends, HTTPException, UploadFile
from controllers.product_controller import ProductController
from controllers.product_image_controller import ProductImageController
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
    product_name: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    rating: Optional[float] = None,
    discount: Optional[int] = None,
    category: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
):
    return ProductController.read_product(
        product_name=product_name,
        price_min=price_min,
        price_max=price_max,
        rating=rating,
        discount=discount,
        category=category,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )


@product.get("/products/carousel/{limit}")
async def get_products_carousel(limit: int = 5):
    return ProductController.products_carousel(limit)


@product.post("/products/upload_images")
async def upload_product_image(
    user: user_dependency, product_id: int, files: List[UploadFile]
):
    return await ProductImageController.upload_product_images(user, product_id, files)


@product.get("/product/product_images")
async def get_product_images(product_id: int):
    return ProductImageController.get_product_images(product_id)


@product.delete("/products/product_images/{product_id}/{image_id}")
async def delete_product_image(product_id: int, image_id: int, user: user_dependency):
    return ProductImageController.delete_product_image(product_id, image_id, user)
