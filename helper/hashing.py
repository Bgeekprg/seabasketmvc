from passlib.context import CryptContext
from config.db_config import SessionLocal
from helper.api_helper import APIHelper
from dtos.auth_models import UserModel
from utils.db_helper import DBHelper

hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def get_hash(text: str):
        return hash_context.hash(text)

    def verify(plain_text: str, hashed_text: str):
        return hash_context.verify(plain_text, hashed_text)

    def authenticate_user(username: str, password: str) -> UserModel:
        user = DBHelper.get_user_by_email(username)
        if user is None:
            user = DBHelper.get_user_by_mobile(username)

        if user is None:
            return APIHelper.send_unauthorized_error(
                errorMessageKey="translations.INVALID_CREDENTIAL"
            )

        if not user.status:
            return APIHelper.send_unauthorized_error(
                errorMessageKey="translations.BLOCKED_USER"
            )

        if not Hash.verify(password, user.password):
            return APIHelper.send_unauthorized_error(
                errorMessageKey="translations.INVALID_CREDENTIAL"
            )

        return UserModel(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role,
        )
