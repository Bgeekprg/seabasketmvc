from typing import Annotated
from fastapi import APIRouter, Depends, status
from config.db_config import SessionLocal
from controllers.order_controller import OrderController
from dtos.auth_models import UserModel
from dtos.orders_models import OrderCreateModel
from helper.token_helper import TokenHelper

order = APIRouter(tags=["Orders"])
user_dependency = Annotated[UserModel, Depends(TokenHelper.get_current_user)]


@order.get("/orders")
def get_all_orders(user: user_dependency, page: int = 1, limit: int = 10):
    return OrderController.get_orders(user, page, limit)


@order.get("/orders/{order_id}")
def get_order_details(user: user_dependency, order_id: int):
    return OrderController.get_order_details(user, order_id)


@order.post("/orders")
def create_order(user: user_dependency, order_data: OrderCreateModel):
    return OrderController.create_order(user, order_data)


@order.put("/orders/{order_id}")
def update_order(user: user_dependency, order_id: int, status: str):
    return OrderController.update_order_status(user, order_id, status)
