from config.db_config import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, ForeignKey, func


class ProductImage(Base):
    __tablename__ = "product_images"
    id = Column(Integer, primary_key=True, index=True)
    productId = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    imageUrl = Column(String(255), nullable=False)
    createdAt = Column(TIMESTAMP, default=func.current_timestamp())
    updatedAt = Column(
        TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )
