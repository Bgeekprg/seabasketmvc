from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class CategoryStatus(str, Enum):
    active = "active"
    inactive = "inactive"


class CategoryModel(BaseModel):
    id: int
    categoryName: str
    status: CategoryStatus
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    category_name: str = Field(..., title="Category name")
    status: CategoryStatus = Field(title="Category status", default="active")


class CategoryUpdate(BaseModel):
    category_name: Optional[str] = Field(title="Category name", default=None)
    status: Optional[CategoryStatus] = Field(title="Category status", default=None)

    class Config:
        from_attributes = True
