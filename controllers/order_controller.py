from fastapi import HTTPException
import i18n
from sqlalchemy import desc
from dtos.auth_models import UserModel
from dtos.orders_models import OrderCreateModel, OrderModel
from helper.admin_helper import ADMINHelper
from helper.api_helper import APIHelper
from models.carts_table import Cart
from models.orders_table import Order
from models.order_details_table import OrderDetail
from config.db_config import SessionLocal
from models.products_table import Product


class OrderController:

    def get_orders(user: UserModel):
        db = SessionLocal()
        orders = (
            db.query(Order)
            .filter(Order.userId == user.id)
            .order_by(desc(Order.id))
            .all()
        )
        db.close()
        return [
            OrderModel(
                orderId=order.id,
                userId=order.userId,
                status=order.status,
                orderStatus=order.orderStatus,
                shippingAddress=order.shippingAddress,
                totalAmount=order.totalAmount,
                paymentStatus=order.paymentStatus,
                createdAt=order.createdAt,
                updatedAt=order.updatedAt,
            )
            for order in orders
        ]

    def get_order_details(user: UserModel, order_id: int):
        db = SessionLocal()
        order = (
            db.query(Order)
            .filter(Order.userId == user.id, Order.id == order_id)
            .first()
        )
        if not order:
            raise HTTPException(
                status_code=404, detail=i18n.t("translations.ORDER_NOT_FOUND")
            )
        order_details = (
            db.query(OrderDetail).filter(OrderDetail.orderId == order_id).all()
        )
        db.close()
        return order_details

    def create_order(user: UserModel, order_data: OrderCreateModel):
        with SessionLocal() as db:
            # Fetch all cart items for the user
            cart_items = db.query(Cart).filter(Cart.userId == user.id).all()
            if not cart_items:
                raise HTTPException(
                    status_code=404, detail=i18n.t("translations.CART_EMPTY")
                )

            # Extract product IDs from the cart items and fetch the products with their stock quantities
            product_ids = [item.productId for item in cart_items]
            products = db.query(Product).filter(Product.id.in_(product_ids)).all()

            # Create a mapping from product ID to product object for quick access
            product_map = {product.id: product for product in products}

            total_price = 0
            order_details = []

            # Check product stock and calculate total price
            for item in cart_items:
                product = product_map.get(item.productId)

                if not product:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Product with ID {item.productId} not found.",
                    )

                discount_price = product.price - (
                    product.price * product.discount / 100
                )
                total_price += discount_price * item.quantity

                # Check if the product has enough stock
                if product.stockQuantity < item.quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Not enough stock for product {product.name}. Available stock: {product.stockQuantity}",
                    )

                order_details.append(
                    OrderDetail(
                        productId=product.id,
                        quantity=item.quantity,
                        price=discount_price,
                        discount=product.price - discount_price,
                    )
                )

            # Create the order
            order = Order(
                userId=user.id,
                totalAmount=total_price,
                shippingAddress=order_data.address,
            )
            db.add(order)
            db.flush()

            # Update stock quantities and add order details
            for detail in order_details:
                detail.orderId = order.id
                db.add(detail)

                # Update stock quantity for the product
                product = product_map.get(detail.productId)
                if product:
                    product.stockQuantity -= detail.quantity
                    db.add(product)

            # Empty the user's cart after the order is placed
            db.query(Cart).filter(Cart.userId == user.id).delete()

            db.commit()

            return APIHelper.send_success_response(
                successMessageKey="translations.ORDER_CREATED",
            )

    def update_order_status(user: UserModel, order_id: int, status: str):
        if ADMINHelper.isAdmin(user):
            pass
        db = SessionLocal()
        order = (
            db.query(Order)
            .filter(Order.userId == user.id, Order.id == order_id)
            .first()
        )
        if not order:
            raise HTTPException(
                status_code=404, detail=i18n.t("translations.ORDER_NOT_FOUND")
            )

        order.status = status
        db.commit()
        db.close()
        return APIHelper.send_success_response(
            successMessageKey="translations.ORDER_STATUS_UPDATED",
        )
