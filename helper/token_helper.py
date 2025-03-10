from jose import JWTError, jwt
from datetime import datetime, timedelta
from dtos.auth_models import UserModel
from helper.api_helper import APIHelper
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import os
from utils.db_helper import DBHelper
from dotenv import load_dotenv

load_dotenv()

# JWT Configuration

"""Please generate a new JWT_SECRET `using openssl rand -hex 32` command and add it in the .env file"""

# Initializing the Hashing alogorith
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


class TokenHelper:
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now() + timedelta(days=1)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_token(token: str):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
            print(f"user_id {payload}")
            user_id: int = payload.get("id")
            if user_id is None:
                return APIHelper.send_unauthorized_error(
                    errorMessageKey="translations.UNAUTHORIZED"
                )
        except JWTError:
            return APIHelper.send_unauthorized_error(
                errorMessageKey="translations.UNAUTHORIZED"
            )
        user = DBHelper.get_user_by_id(user_id)
        if user is None:
            return APIHelper.send_unauthorized_error(
                errorMessageKey="translations.UNAUTHORIZED"
            )
        return UserModel(id=user.id,email=user.email,name=user.name,role=user.role)

    def get_current_user(token=Depends(oauth2_scheme)) -> UserModel:
        return TokenHelper.verify_token(token)
