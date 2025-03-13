from decimal import Decimal
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class CreateReviewRatingModel(BaseModel):
    rating: Optional[Decimal] = None
    review: str


class EditReviewRatingModel(BaseModel):
    rating: Optional[Decimal] = None
    review: Optional[str] = None


class ReviewRatingResponseModel(BaseModel):
    id: int
    rating: Optional[Decimal] = 0
    review: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: int
    product_id: int
    product_name: str
