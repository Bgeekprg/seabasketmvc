from sqlalchemy import DECIMAL, TIMESTAMP, Column, ForeignKey, Integer, func
from config.db_config import Base
from sqlalchemy.orm import relationship
from models.products_table import Product


class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, autoincrement=True)
    orderId = Column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    productId = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    quantity = Column(Integer, default=1)
    price = Column(DECIMAL(10, 2), nullable=False)
    discount = Column(DECIMAL(7, 2), default=0)
    createdAt = Column(TIMESTAMP, default=func.current_timestamp(), nullable=False)
    updatedAt = Column(TIMESTAMP, onupdate=func.current_timestamp(), nullable=True)

    product = relationship("Product", backref="order_detail_product", lazy="joined")
