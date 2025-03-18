import locale
from fastapi import Depends, HTTPException, status
from config.db_config import SessionLocal
from dtos.auth_models import UserModel
from dtos.base_response_model import BaseResponseModel
from helper.admin_helper import ADMINHelper
from helper.api_helper import APIHelper
from helper.token_helper import TokenHelper
from models.categories_table import Category
from dtos.categories_models import CategoryCreate, CategoryModel, CategoryUpdate
import i18n


class CategoryController:
    def get_categories(id, status):
        with SessionLocal() as db:
            if id:
                return db.query(Category).filter(Category.id == id).first()
            if status != None:
                return db.query(Category).filter(Category.status == status).all()

            return db.query(Category).all()

    def create_category(
        categories: CategoryCreate,
        user: UserModel,
    ) -> BaseResponseModel:
        if ADMINHelper.isAdmin(user):
            with SessionLocal() as db:
                try:
                    new_category = Category(
                        categoryName=categories.category_name, status=categories.status
                    )
                    db.add(new_category)
                    db.commit()
                    db.refresh(new_category)
                    return APIHelper.send_success_response(
                        data=CategoryModel(
                            id=new_category.id,
                            categoryName=new_category.categoryName,
                            status=new_category.status,
                        ),
                        successMessageKey="translations.CATEGORY_CREATED",
                    )
                except:
                    db.rollback()

    def update_category(
        category_id: int, category: CategoryUpdate, user: UserModel
    ) -> BaseResponseModel:
        with SessionLocal() as db:
            if ADMINHelper.isAdmin(user):

                category_to_update = (
                    db.query(Category).filter(Category.id == category_id).first()
                )
                if category_to_update:
                    if category.category_name is not None:
                        category_to_update.categoryName = category.category_name
                    if category.status is not None:
                        category_to_update.status = category.status

                    db.commit()
                    db.refresh(category_to_update)
                    return APIHelper.send_success_response(
                        data=CategoryModel(
                            id=category_to_update.id,
                            categoryName=category_to_update.categoryName,
                            status=category_to_update.status,
                            created_at=category_to_update.createdAt,
                            updated_at=category_to_update.updatedAt,
                        ),
                        successMessageKey="translations.CATEGORY_UPDATED",
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=(
                            i18n.t(
                                key="translations.CATEGORY_NOT_EXIST",
                                locale=locale,
                            )
                        ),
                    )

            else:
                return APIHelper.send_error_response(
                    errorMessageKey="translations.PERMISSION_DENIED",
                )

    def delete_category(category_id: int, user: UserModel) -> BaseResponseModel:
        with SessionLocal() as db:
            if ADMINHelper.isAdmin(user):
                category_to_delete = (
                    db.query(Category).filter(Category.id == category_id).first()
                )

                if not category_to_delete:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.CATEGORY_NOT_EXIST",
                     )

                try:
                    db.delete(category_to_delete)
                    db.commit()
                    return APIHelper.send_success_response(
                        data=None,
                        successMessageKey="translations.CATEGORY_DELETED",
                    )
                except Exception as e:
                    db.rollback()
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.CATEGORY_DELETE_FAILED",
                    )
