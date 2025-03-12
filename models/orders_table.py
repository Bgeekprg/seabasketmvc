from sqlalchemy import (
    DECIMAL,
    TEXT,
    TIMESTAMP,
    Boolean,
    Column,
    Enum,
    ForeignKey,
    Integer,
    func,
)
from config.db_config import Base
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(Boolean, default=True)
    totalAmount = Column(DECIMAL(10, 2), nullable=False)
    orderStatus = Column(
        Enum("pending", "shipped", "delivered", "cancelled", name="order_status"),
        default="pending",
    )
    paymentStatus = Column(
        Enum("pending", "paid", "failed", "refunded", name="payment_status"),
        default="pending",
    )
    shippingAddress = Column(TEXT, nullable=False)
    createdAt = Column(TIMESTAMP, default=func.current_timestamp(), nullable=False)
    updatedAt = Column(
        TIMESTAMP,
        onupdate=func.current_timestamp(),
        nullable=True,
    )

    orderDetails = relationship("OrderDetail", backref="order", lazy="selectin")
    user = relationship("User", backref="orders", lazy="selectin")
