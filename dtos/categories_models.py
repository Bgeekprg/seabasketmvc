from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class CategoryModel(BaseModel):
    id: int
    categoryName: str
    status: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    category_name: str = Field(..., title="Category name")
    status: bool = Field(title="Category status", default=True)


class CategoryUpdate(BaseModel):
    category_name: Optional[str] = Field(title="Category name", default=None)
    status: Optional[bool] = Field(title="Category status", default=None)

    class Config:
        from_attributes = True
