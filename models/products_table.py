from sqlalchemy import TIMESTAMP, Enum, String, DECIMAL, Column, func, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer, Text, Boolean
from config.db_config import meta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config.db_config import Base
from models.categories_table import Category


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    stockQuantity = Column(Integer, default=0)
    price = Column(DECIMAL(10, 2), nullable=False)
    categoryId = Column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=True
    )
    productUrl = Column(String(255), nullable=True)
    discount = Column(Integer, nullable=True)
    rating = Column(DECIMAL(3, 2), nullable=True)
    isAvailable = Column(Boolean, default=True)
    createdAt = Column(TIMESTAMP, default=func.current_timestamp())
    updatedAt = Column(
        TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )
