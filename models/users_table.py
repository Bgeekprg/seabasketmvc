# Importing libraries
from sqlalchemy import Enum, String, Table, Column, func
from sqlalchemy.sql.sqltypes import DateTime, Integer, Text, Boolean
from config.db_config import meta
from sqlalchemy.ext.declarative import declarative_base
from config.db_config import Base

# Initializing
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    phoneNumber = Column(String(13), unique=True, index=True)
    password = Column(String(80), nullable=False)
    profilePic = Column(String(255), nullable=True)
    role = Column(
        Enum("customer", "admin", name="role"),
        default="customer",
        nullable=False,
    )
    status = Column(Boolean, default=True)
    isVerified = Column(Boolean, default=False)
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())
    