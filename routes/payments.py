import logging
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Request
import stripe
from sqlalchemy.orm import Session
from controllers.payment_controller import PaymentController
from dtos.auth_models import UserModel
from models.payments_table import Payment
from models.orders_table import Order
from config.db_config import SessionLocal
from decimal import Decimal
from dotenv import load_dotenv
from helper.token_helper import TokenHelper
import os

payment = APIRouter(tags=["Payment"])
user_dependency = Annotated[UserModel, Depends(TokenHelper.get_current_user)]

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@payment.get("/payments/{order_id}")
async def get_payment_details_page(request: Request, order_id: int):
    return PaymentController.get_payment_details_page(request, order_id)

@payment.post("/payment/confirm/{order_id}")
async def confirm_payment(order_id: int, request: Request):
    return await PaymentController.confirm_payment(order_id, request)