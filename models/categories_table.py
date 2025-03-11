from sqlalchemy import TIMESTAMP, Column
from sqlalchemy import String, Column, func
from sqlalchemy.sql.sqltypes import Integer, Boolean
from config.db_config import meta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config.db_config import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    categoryName = Column(String(100), nullable=False)
    status = Column(Boolean, default=True)
    createdAt = Column(TIMESTAMP, default=func.current_timestamp())
    updatedAt = Column(
        TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )

    products = relationship(
        "Product", back_populates="category", cascade="all, delete-orphan"
    )
