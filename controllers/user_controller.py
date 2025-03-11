import logging
from fastapi import HTTPException, status
import i18n
from config.db_config import SessionLocal
from dtos.auth_models import UserModel
from dtos.password_models import PasswordChangeModel
from dtos.user_models import UserResponseModel
from helper.admin_helper import ADMINHelper
from helper.api_helper import APIHelper
from helper.hashing import Hash
from models.users_table import User
from sqlalchemy.exc import SQLAlchemyError


class UserController:
    def get_user_list(user: UserModel, status: bool = None):
        if ADMINHelper.isAdmin(user):
            try:
                with SessionLocal() as db:
                    if status is not None:
                        users = (
                            db.query(User)
                            .filter(User.status == status, User.role == "customer")
                            .all()
                        )
                    else:
                        users = db.query(User).filter(User.role == "customer").all()
                    return [
                        UserResponseModel(
                            email=user.email,
                            name=user.name,
                            role=user.role,
                            status=user.status,
                        )
                        for user in users
                    ]
            except SQLAlchemyError as e:
                logging.error(e)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database error occurred.",
                )

    def get_user_profile(user: UserModel):
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user.id).first()

        return user

    def change_password(user: UserModel, password: PasswordChangeModel):
        with SessionLocal() as db:
            existing_user = db.query(User).filter(User.id == user.id).first()
            if existing_user:
                if Hash.verify(password.old_password, existing_user.password):
                    existing_user.password = Hash.get_hash(password.new_password)
                    db.commit()

                    return APIHelper.send_success_response(
                        successMessageKey="translations.PASSWORD_CHANGED"
                    )
                else:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.WRONG_PASSWORD"
                    )
