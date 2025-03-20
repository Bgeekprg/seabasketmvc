import logging
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import stripe
from sqlalchemy.orm import Session
from models.order_details_table import OrderDetail
from models.payments_table import Payment
from models.orders_table import Order
from config.db_config import SessionLocal
from dotenv import load_dotenv
import os

templates = Jinja2Templates(directory="templates")
load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class PaymentController:
    def get_payment_details_page(request: Request, order_id: int):
        try:
            with SessionLocal() as db:
                order = db.query(Order).filter(Order.id == order_id).first()
                if not order:
                    raise HTTPException(status_code=404, detail="Order not found")

                if order.paymentStatus == "paid":
                    raise HTTPException(status_code=400, detail="Order already paid")

                order_details = (
                    db.query(OrderDetail).filter(OrderDetail.orderId == order_id).all()
                )

                return templates.TemplateResponse(
                    "payment_form.html",
                    {
                        "request": request,
                        "order_id": order_id,
                        "order_details": order_details,
                        "stripe_publishable_key": os.getenv("STRIPE_PUBLIC_KEY"),
                    },
                )

        except stripe.error.StripeError as e:
            logging.error(f"StripeError occurred: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def confirm_payment(order_id: int, request: Request):
        db = SessionLocal()
        try:

            body = await request.json()
            logging.info(f"Received request body: {body}")
            payment_method_id = body.get("payment_method")
            if not payment_method_id:
                raise HTTPException(
                    status_code=400, detail="Payment method ID is missing"
                )

            order = db.query(Order).filter(Order.id == order_id).first()
            logging.info(
                f"Order found: {order.id if order else None}, Status: {order.paymentStatus if order else None}"
            )
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")

            if order.paymentStatus == "paid":
                raise HTTPException(status_code=400, detail="Order already paid")

            amount = int(float(order.totalAmount) * 100)
            logging.info(
                f"Creating PaymentIntent with amount: {amount}, payment_method: {payment_method_id}"
            )
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency="inr",
                payment_method=payment_method_id,
                confirm=True,
                description=f"Payment for Order {order.id}",
                return_url="https://www.google.com",
            )

            if payment_intent.status == "succeeded":
                payment = Payment(
                    userId=order.userId,
                    orderId=order.id,
                    totalAmount=order.totalAmount,
                    transactionId=payment_intent.id,
                    status="paid",
                )
                db.add(payment)
                order.paymentStatus = "paid"
                db.commit()
                return JSONResponse(
                    content={
                        "message": "Payment succeeded and order updated.",
                        "payment_intent_id": payment_intent.id,
                    },
                    status_code=200,
                )
            elif payment_intent.status == "requires_action":
                return JSONResponse(
                    content={
                        "message": "Payment requires additional action",
                        "payment_intent_id": payment_intent.id,
                        "client_secret": payment_intent.client_secret,
                        "status": payment_intent.status,
                    },
                    status_code=200,
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Payment failed with status: {payment_intent.status}",
                )

        except stripe.error.StripeError as e:
            logging.error(f"StripeError occurred: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except ValueError as e:
            logging.error(f"ValueError occurred: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid amount format")
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            db.close()
