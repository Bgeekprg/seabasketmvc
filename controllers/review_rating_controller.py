from fastapi import HTTPException, status
import i18n
from config.db_config import SessionLocal
from dtos.auth_models import UserModel
from dtos.review_rating_models import (
    CreateReviewRatingModel,
    EditReviewRatingModel,
    ReviewRatingResponseModel,
)
from helper.api_helper import APIHelper
from models.order_details_table import OrderDetail
from models.orders_table import Order
from models.products_table import Product
from models.reviews_ratings_table import ReviewRating
from sqlalchemy import func


class ReviewRatingController:
    def get_review_ratings(product_id: int, page: int = 1, limit: int = 10):
        with SessionLocal() as db:
            try:
                offset = (page - 1) * limit
                review_ratings = (
                    db.query(ReviewRating)
                    .filter(ReviewRating.productId == product_id)
                    .offset(offset)
                    .limit(limit)
                    .all()
                )

                return review_ratings
            except Exception as e:
                return {"error": str(e)}

    def create_review_rating(
        user: UserModel, product_id: int, review_rating: CreateReviewRatingModel
    ):
        with SessionLocal() as db:
            try:
                existing_review = (
                    db.query(ReviewRating)
                    .filter(
                        ReviewRating.userId == user.id,
                        ReviewRating.productId == product_id,
                    )
                    .first()
                )
                if existing_review:
                    return {"message": i18n.t(key="translations.ALREADY_GIVEN_REVIEW")}

                has_order = (
                    db.query(Order)
                    .join(OrderDetail, Order.id == OrderDetail.orderId)
                    .filter(
                        Order.userId == user.id,
                        OrderDetail.productId == product_id,
                        Order.orderStatus == "delivered",
                    )
                    .first()
                )
                if not has_order:
                    return {
                        "message": "You must purchase this product before leaving a review."
                    }

                reviewRating = ReviewRating(
                    userId=user.id,
                    productId=product_id,
                    rating=review_rating.rating,
                    reviewText=review_rating.review,
                )
                db.add(reviewRating)
                db.commit()
                db.refresh(reviewRating)

                avg_rating = (
                    db.query(func.avg(ReviewRating.rating))
                    .filter(ReviewRating.productId == product_id)
                    .scalar()
                )

                product = db.query(Product).filter(Product.id == product_id).first()
                if product:
                    product.rating = avg_rating
                    db.commit()

                review_ratings_return = ReviewRatingResponseModel(
                    id=reviewRating.id,
                    product_name=product.name,
                    rating=reviewRating.rating,
                    review=reviewRating.reviewText,
                    user_id=reviewRating.userId,
                    product_id=reviewRating.productId,
                    created_at=reviewRating.createdAt,
                )

                return APIHelper.send_success_response(
                    data=review_ratings_return, successMessageKey="translations.SUCCESS"
                )

            except Exception as e:
                db.rollback()
                return {"error": str(e)}

    def edit_review_ratings(
        user: UserModel, product_id: int, review_rating: EditReviewRatingModel
    ):

        with SessionLocal() as db:
            reviews = (
                db.query(ReviewRating)
                .filter(
                    ReviewRating.userId == user.id,
                    ReviewRating.productId == product_id,
                )
                .first()
            )
            if not reviews:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=i18n.t(key="translations.USER_REVIEW_NOT_EXIST"),
                )

            if review_rating.review != None:
                reviews.reviewText = review_rating.review

            if review_rating.rating != None and (
                review_rating.rating >= 0 and review_rating.rating <= 5
            ):
                reviews.rating = review_rating.rating
            if review_rating.rating == None and review_rating.review == None:
                return APIHelper.send_error_response(
                    errorMessageKey="translations.REVIEW_OR_RATING_REQUIRED"
                )
            avg_rating = (
                db.query(func.avg(ReviewRating.rating))
                .filter(ReviewRating.productId == product_id)
                .scalar()
            )

            product = db.query(Product).filter(Product.id == product_id).first()
            product.rating = avg_rating
            db.commit()

            review_ratings_return = ReviewRatingResponseModel(
                id=reviews.id,
                product_name=product.name,
                rating=reviews.rating,
                review=reviews.reviewText,
                user_id=reviews.userId,
                product_id=reviews.productId,
                created_at=reviews.createdAt,
            )

            return APIHelper.send_success_response(
                data=review_ratings_return,
                successMessageKey="translations.SUCCESS",
            )

    def delete_review_rating(user: UserModel, product_id: int):
        with SessionLocal() as db:
            reviews = (
                db.query(ReviewRating)
                .filter(
                    ReviewRating.productId == product_id, ReviewRating.userId == user.id
                )
                .first()
            )
            if reviews:
                db.delete(reviews)
                db.commit()
                return APIHelper.send_success_response(
                    successMessageKey="translations.REVIEW_DELETED"
                )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=i18n.t("translations.USER_REVIEW_NOT_EXIST"),
            )
