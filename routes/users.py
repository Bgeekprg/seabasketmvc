from fastapi import APIRouter, Depends, HTTPException
from controllers.user_controller import UserController
from dtos.auth_models import UserModel
from dtos.password_models import PasswordChangeModel
from dtos.user_models import UserResponseModel
from typing import Annotated, List

from helper.token_helper import TokenHelper

user = APIRouter(tags=["Users"])
user_dependency = Annotated[UserModel, Depends(TokenHelper.get_current_user)]


@user.get("/user", response_model=List[UserResponseModel])
async def list_users(user: user_dependency, status: bool = None):
    return UserController.get_user_list(user, status)


@user.get("/user/profiles")
async def profile(user: user_dependency):
    return UserController.get_user_profile(user)


@user.post("/user/change_password")
async def change_password(user: user_dependency, password: PasswordChangeModel):
    return UserController.change_password(user, password)
