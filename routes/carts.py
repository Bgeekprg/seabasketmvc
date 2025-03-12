from fastapi import APIRouter, Depends, HTTPException, status
from controllers.cart_controller import CartController
from dtos.auth_models import UserModel
from dtos.base_response_model import BaseResponseModel
from dtos.cart_models import CartModel
from helper.token_helper import TokenHelper
from models.carts_table import Cart
from typing import Annotated

cart = APIRouter(tags=["Carts"])
user_dependency = Annotated[UserModel, Depends(TokenHelper.get_current_user)]


@cart.get("/cart")
async def get_cart(user: user_dependency):
    return CartController.get_cart(user)


@cart.post(
    "/cart/{product_id}",
    response_model=BaseResponseModel,
    status_code=status.HTTP_201_CREATED,
)
async def add_to_cart(user: user_dependency, product_id: int):
    return CartController.add_to_cart(user, product_id)


@cart.put("/cart/{cart_id}")
async def decrease_quantity(cart_id: int, user: user_dependency):
    return CartController.decrease_quantity(cart_id, user)


@cart.delete("/cart/{cart_id}")
async def remove_from_cart(cart_id: int, user: user_dependency):
    return CartController.remove_from_cart(cart_id, user)


@cart.delete("/cart")
async def clear_cart(user: user_dependency):
    return CartController.clear_cart(user)
