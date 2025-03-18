import locale
from typing import List
from fastapi import Depends, HTTPException, status
from sqlalchemy import and_, desc
from config.db_config import SessionLocal
from dtos.auth_models import UserModel
from dtos.base_response_model import BaseResponseModel
from dtos.products_models import (
    CreateProductModel,
    ProductListModel,
    ProductModel,
    ProductResponseModel,
    UpdateProductModel,
)
from helper.admin_helper import ADMINHelper
from helper.api_helper import APIHelper
from helper.token_helper import TokenHelper
from models.order_details_table import OrderDetail
from models.orders_table import Order
from models.product_images_table import ProductImage
from models.products_table import Product
from models.categories_table import Category
from dtos.categories_models import *
from sqlalchemy.exc import SQLAlchemyError
import i18n
import logging


class ProductController:

    def read_product(
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
    ) -> List[ProductListModel]:
        try:
            db = SessionLocal()
            query = db.query(Product).filter(Product.isAvailable == True)

            filter_conditions = []
            if product_name:
                filter_conditions.append(Product.name.like(f"%{product_name}%"))
            if price_min is not None:
                filter_conditions.append(Product.price >= price_min)
            if price_max is not None:
                filter_conditions.append(Product.price <= price_max)
            if rating is not None:
                filter_conditions.append(Product.rating >= rating)
            if discount is not None:
                filter_conditions.append(Product.discount >= discount)
            if category is not None:
                filter_conditions.append(Product.categoryId == category)

            if filter_conditions:
                query = query.filter(and_(*filter_conditions))

            if sort_by:
                column = getattr(Product, sort_by, None)
                if column:
                    if sort_order == "descending":
                        query = query.order_by(column.desc())
                    else:
                        query = query.order_by(column)
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid sort field: {sort_by}",
                    )

            offset_value = (page - 1) * page_size
            query = query.offset(offset_value).limit(page_size)

            products = query.all()
            return [
                ProductListModel(
                    id=product.id,
                    name=product.name,
                    stockQuantity=product.stockQuantity,
                    price=product.price,
                    categoryId=product.categoryId,
                    productUrl=product.productUrl,
                    discount=product.discount,
                    rating=product.rating,
                )
                for product in products
            ]
        except Exception as e:
            logging.error(f"Error occurred while fetching products: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred.",
            )

    def create_product(product: CreateProductModel, user: UserModel):
        logger = logging.getLogger(__name__)
        logger.info(f"Creating product with data: {product}")
        if ADMINHelper.isAdmin(user):
            with SessionLocal() as db:
                new_product = Product(**product.model_dump())
                try:
                    logger.info("Adding new product to the database.")
                    db.add(new_product)
                    logger.info("Committing the new product to the database.")
                    db.commit()
                    db.refresh(new_product)
                    product_response = ProductResponseModel(
                        id=new_product.id,
                        name=new_product.name,
                        description=new_product.description,
                        stockQuantity=new_product.stockQuantity,
                        price=new_product.price,
                        categoryId=new_product.categoryId,
                        productUrl=new_product.productUrl,
                        discount=new_product.discount,
                        rating=new_product.rating,
                        isAvailable=new_product.isAvailable,
                        createdAt=new_product.createdAt,
                        updatedAt=new_product.updatedAt,
                    )
                    return APIHelper.send_success_response(
                        successMessageKey=i18n.t("translations.PRODUCT_CREATED"),
                        data=product_response,
                    )

                except SQLAlchemyError as e:
                    db.rollback()
                    logger.error(f"Database error occurred: {str(e)}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Database error occurred: {str(e)}",
                    )
                except Exception as e:
                    db.rollback()
                    logger.error(f"Unexpected error occurred: {str(e)}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Unexpected error occurred: {str(e)}",
                    )

    def read_product_by_id(product_id: int):
        logger = logging.getLogger(__name__)
        logger.info(f"Reading product with ID: {product_id}")
        with SessionLocal() as db:
            product = db.query(Product).filter(Product.id == product_id).first()
            if product:
                product_images = (
                    db.query(ProductImage)
                    .filter(ProductImage.productId == product_id)
                    .all()
                )
                images = [image.imageUrl for image in product_images]
                product_response = ProductResponseModel(
                    id=product.id,
                    name=product.name,
                    description=product.description,
                    stockQuantity=product.stockQuantity,
                    price=product.price,
                    categoryId=product.categoryId,
                    productUrl=product.productUrl,
                    discount=product.discount,
                    rating=product.rating,
                    isAvailable=product.isAvailable,
                    createdAt=product.createdAt,
                    updatedAt=product.updatedAt,
                    images=images,
                )
                return product_response
            else:
                logger.error(f"Product with ID {product_id} not found.")

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=i18n.t("translations.PRODUCT_NOT_EXIST"),
                )

    def update_product(product_id: int, product: UpdateProductModel, user: UserModel):
        logger = logging.getLogger(__name__)
        logger.info(f"Updating product with ID: {product_id}")
        if ADMINHelper.isAdmin(user):
            with SessionLocal() as db:
                try:
                    exist_product = (
                        db.query(Product).filter(Product.id == product_id).first()
                    )
                    if exist_product:
                        for key, value in product.dict().items():
                            if value is not None:
                                setattr(exist_product, key, value)

                        db.commit()
                        db.refresh(exist_product)
                        return exist_product
                    else:
                        logger.error(f"Product with ID {product_id} not found.")
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=i18n.t("translations.PRODUCT_NOT_EXIST"),
                        )
                except SQLAlchemyError as e:
                    logger.error(f"Error updating product: {e}")
                    db.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Database error occurred.",
                    )
                except Exception as e:
                    logger.error(f"Unexpected error occurred: {e}")
                    db.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Unexpected error occurred.",
                    )

    def delete_product(product_id: int, user: UserModel):
        logger = logging.getLogger(__name__)
        logger.info(f"Deleting product with ID: {product_id}")

        if ADMINHelper.isAdmin(user):
            with SessionLocal() as db:
                try:
                    exist_product = (
                        db.query(Product).filter(Product.id == product_id).first()
                    )

                    if exist_product:
                        order_details_to_delete = (
                            db.query(OrderDetail)
                            .filter(OrderDetail.productId == product_id)
                            .all()
                        )

                        for order_detail in order_details_to_delete:
                            db.delete(order_detail)

                        order_ids = [
                            order_detail.orderId
                            for order_detail in order_details_to_delete
                        ]
                        db.query(Order).filter(Order.id.in_(order_ids)).delete(
                            synchronize_session=False
                        )

                        db.delete(exist_product)

                        db.commit()

                        return APIHelper.send_success_response(
                            successMessageKey=i18n.t("translations.PRODUCT_DELETED"),
                        )
                    else:
                        logger.error(f"Product with ID {product_id} not found.")
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=i18n.t("translations.PRODUCT_NOT_EXIST"),
                        )

                except SQLAlchemyError as e:
                    logger.error(f"Error deleting product: {e}")
                    db.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Database error occurred.",
                    )
                except Exception as e:
                    logger.error(f"Unexpected error occurred: {e}")
                    db.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Unexpected error occurred.",
                    )

    def products_carousel(limit: int):
        logger = logging.getLogger(__name__)
        logger.info("Getting products carousel")
        with SessionLocal() as db:
            try:
                products = (
                    db.query(Product).order_by(desc(Product.rating)).limit(limit).all()
                )

                return APIHelper.send_success_response(
                    data=[
                        ProductListModel(
                            id=product.id,
                            name=product.name,
                            stockQuantity=product.stockQuantity,
                            price=product.price,
                            categoryId=product.categoryId,
                            productUrl=product.productUrl,
                            discount=product.discount,
                            rating=product.rating,
                        )
                        for product in products
                    ],
                    successMessageKey=i18n.t("translations.SUCCESS"),
                )
            except SQLAlchemyError as e:
                logger.error(f"Error getting products carousel: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database error occurred.",
                )
            except Exception as e:
                logger.error(f"Unexpected error occurred: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Unexpected error occurred.",
                )
