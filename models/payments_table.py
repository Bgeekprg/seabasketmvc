from fastapi import APIRouter

from sqlalchemy import (
    DECIMAL,
    TEXT,
    TIMESTAMP,
    Boolean,
    Column,
    Enum,
    ForeignKey,
    Integer,
    String,
    func,
)
from config.db_config import Base
from sqlalchemy.orm import relationship


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    orderId = Column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    totalAmount = Column(DECIMAL(10, 2), nullable=False)
    transactionId = Column(String(255), nullable=False)
    status = Column(
        Enum("paid", "unpaid", "refunded", "failed", name="status"),
        default="unpaid",
        nullable=False,
    )
    createdAt = Column(TIMESTAMP, default=func.current_timestamp(), nullable=False)
    updatedAt = Column(TIMESTAMP, onupdate=func.current_timestamp(), nullable=True)
