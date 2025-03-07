# Importing libraries
from dtos.auth_models import TokenModel, UserModel
from dtos.base_response_model import BaseResponseModel
from dtos.user_models import CreateUserModel
from helper.api_helper import APIHelper
from helper.token_helper import TokenHelper
from helper.hashing import Hash
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from config.db_config import SessionLocal, engine
from models.users_table import User
from utils.db_helper import DBHelper


class AuthController:
    def login(request: OAuth2PasswordRequestForm):
        user = Hash.authenticate_user(
            username=request.username, password=request.password
        )
        access_token = TokenHelper.create_access_token(user.dict())
        response = TokenModel(
            access_token=access_token,
            token_type="Bearer",
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role,
        )
        return APIHelper.send_success_response(
            data=response, successMessageKey="translations.LOGIN_SUCCESS"
        )

    def register(user_data: CreateUserModel):
        user = DBHelper.get_user_by_email(user_data.email)
        if not user:
            with SessionLocal() as db:
                try:
                    new_user = User(
                        email=user_data.email,
                        password=Hash.get_hash(user_data.password),
                        name=user_data.name,
                        role=user_data.role,
                        status=user_data.status,
                    )
                    db.add(new_user)
                    db.commit()
                    return APIHelper.send_success_response(
                        successMessageKey="translations.REGISTER_SUCCESS"
                    )
                except Exception as e:
                    db.rollback()
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.USER_EXIST"
                    )
        else:
            return APIHelper.send_error_response(
                errorMessageKey="translations.USER_EXIST"
            )
