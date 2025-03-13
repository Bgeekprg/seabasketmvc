from decimal import Decimal
from sqlalchemy import Numeric, create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

from config.db_config import Base


class ReviewRating(Base):
    __tablename__ = "reviews_ratings"
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    productId = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    rating = Column(Numeric, nullable=True,default=0)
    reviewText = Column(String, nullable=True)
    createdAt = Column(DateTime, default=datetime.now)
    updatedAt = Column(DateTime, default=datetime.now, onupdate=datetime.now)
