from config.db_config import Base
from sqlalchemy import TIMESTAMP, Column, Integer, ForeignKey, func
from sqlalchemy.orm import relationship
from models.products_table import Product
from models.users_table import User


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    productId = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    quantity = Column(Integer, default=1)
    createdAt = Column(TIMESTAMP, default=func.current_timestamp())
    updatedAt = Column(
        TIMESTAMP,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )

    # user = relationship("User", backref="cart_user", lazy="joined")
    product = relationship("Product", backref="cart_product", lazy="joined")
