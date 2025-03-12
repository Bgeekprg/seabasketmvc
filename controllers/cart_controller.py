from fastapi import HTTPException, status
import i18n
from config.db_config import SessionLocal
from dtos.auth_models import UserModel
from dtos.base_response_model import BaseResponseModel
from dtos.cart_models import CartModel, CartResponseModel
from helper.api_helper import APIHelper
from models.carts_table import Cart
from models.products_table import Product
import logging


class CartController:
    def get_cart(user: UserModel):
        db = SessionLocal()
        try:
            cart_items = db.query(Cart).filter(Cart.userId == user.id).all()
            db.close()
            return [
                CartResponseModel(
                    id=item.id,
                    user_id=item.userId,
                    product_id=item.productId,
                    quantity=item.quantity,
                    price=item.product.price
                    - (item.product.discount * item.product.price / 100),
                    product_name=item.product.name,
                )
                for item in cart_items
            ]

        except Exception as e:
            logging.error(f"Error in get_cart: {e}")
            db.close()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    def add_to_cart(user: UserModel, product_id: int) -> BaseResponseModel:
        logger = logging.getLogger(__name__)
        with SessionLocal() as db:
            try:
                existing_product = (
                    db.query(Product).filter(Product.id == product_id).first()
                )
                if not existing_product:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=i18n.t(key="translations.PRODUCT_NOT_FOUND"),
                    )

                existing_cart_item = (
                    db.query(Cart)
                    .filter(Cart.userId == user.id, Cart.productId == product_id)
                    .first()
                )

                if existing_cart_item:
                    existing_cart_item.quantity += 1
                    db.commit()
                    db.refresh(existing_cart_item)
                    cart_response = CartResponseModel(
                        id=existing_cart_item.id,
                        user_id=existing_cart_item.userId,
                        product_id=existing_cart_item.productId,
                        quantity=existing_cart_item.quantity,
                        price=existing_cart_item.product.price
                        - (
                            existing_cart_item.product.discount
                            * existing_cart_item.product.price
                            / 100
                        ),
                        product_name=existing_product.name,
                    )
                    logger.info(f"Updated cart item: {cart_response}")
                    return APIHelper.send_success_response(
                        data=cart_response.model_dump(),
                        successMessageKey="translations.PRODUCT_QTY_UPDATED",
                    )
                else:
                    new_cart_item = Cart(
                        userId=user.id, productId=product_id, quantity=1
                    )
                    db.add(new_cart_item)
                    db.commit()
                    db.refresh(new_cart_item)

                    cart_response = CartResponseModel(
                        id=new_cart_item.id,
                        user_id=new_cart_item.userId,
                        product_id=new_cart_item.productId,
                        quantity=new_cart_item.quantity,
                        price=new_cart_item.product.price
                        - (
                            new_cart_item.product.discount
                            * new_cart_item.product.price
                            / 100
                        ),
                        product_name=existing_product.name,
                    )
                    logger.info(f"Created new cart item: {cart_response}")
                    return APIHelper.send_success_response(
                        data=cart_response.model_dump(),
                        successMessageKey="translations.PRODUCT_ADDED_CART",
                    )

            except Exception as e:
                logger.error(f"Error in add_to_cart: {str(e)}")
                return APIHelper.send_error_response(errorMessageKey=str(e))

    def decrease_quantity(cart_id: int, user: UserModel):
        with SessionLocal() as db:
            cart_item = db.query(Cart).filter(Cart.id == cart_id).first()
            if not cart_item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=i18n.t(key="translations.CART_ITEM_NOT_FOUND"),
                )

            if cart_item.userId != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=i18n.t(key="translations.UNAUTHORIZED"),
                )

            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                db.commit()
                db.refresh(cart_item)
                return APIHelper.send_success_response(
                    data=CartResponseModel(
                        id=cart_item.id,
                        user_id=cart_item.userId,
                        product_id=cart_item.productId,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                        - (cart_item.product.discount * cart_item.product.price / 100),
                        product_name=cart_item.product.name,
                    ).model_dump(),
                    successMessageKey="translations.PRODUCT_QTY_UPDATED",
                )
            else:
                db.delete(cart_item)
                db.commit()
                return APIHelper.send_success_response(
                    data=None,
                    successMessageKey="translations.PRODUCT_REMOVED_CART",
                )

    def remove_from_cart(cart_id: int, user: UserModel):
        with SessionLocal() as db:
            cart_item = db.query(Cart).filter(Cart.id == cart_id).first()
            if not cart_item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=i18n.t(key="translations.CART_ITEM_NOT_FOUND"),
                )
            if cart_item.userId != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=i18n.t(key="translations.UNAUTHORIZED"),
                )
            db.delete(cart_item)
            db.commit()
            return APIHelper.send_success_response(
                data=None, successMessageKey="translations.PRODUCT_REMOVED_CART"
            )

    def clear_cart(user: UserModel):
        with SessionLocal() as db:
            cart_items = db.query(Cart).filter(Cart.userId == user.id).all()
            if not cart_items:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=i18n.t(key="translations.CART_EMPTY"),
                )
            for cart_item in cart_items:
                db.delete(cart_item)
                db.commit()
            return APIHelper.send_success_response(
                data=None, successMessageKey="translations.CART_CLEARED"
            )
