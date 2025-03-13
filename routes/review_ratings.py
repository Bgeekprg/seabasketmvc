from typing import Annotated
from fastapi import APIRouter, Depends, status
from controllers.review_rating_controller import ReviewRatingController
from dtos.auth_models import UserModel
from dtos.review_rating_models import CreateReviewRatingModel, EditReviewRatingModel
from helper.token_helper import TokenHelper

review_rating = APIRouter(tags=["Review_Rating"])
user_dependency = Annotated[UserModel, Depends(TokenHelper.get_current_user)]


@review_rating.get("/review_rating/{product_id}")
async def get_review_rating(product_id: int, page: int = 1, limit: int = 10):
    return ReviewRatingController.get_review_ratings(product_id, page, limit)


@review_rating.post("/review_rating/{product_id}")
async def create_review_rating(
    user: user_dependency, product_id: int, review_rating: CreateReviewRatingModel
):
    return ReviewRatingController.create_review_rating(user, product_id, review_rating)


@review_rating.put("/review_rating/{product_id}")
async def edit_review_rating(
    user: user_dependency, product_id: int, review_rating: EditReviewRatingModel
):
    return ReviewRatingController.edit_review_ratings(user, product_id, review_rating)


@review_rating.delete("/review_rating/{product_id}")
async def delete_review_rating(user: user_dependency, product_id: int):
    return ReviewRatingController.delete_review_rating(user, product_id)
