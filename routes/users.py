from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from config.db_config import SessionLocal
from controllers.user_controller import UserController
from dtos.auth_models import UserModel
from dtos.password_models import PasswordChangeModel
from dtos.user_models import UserResponseModel, UserUpdateModel
from typing import Annotated, List
from fastapi.templating import Jinja2Templates
from datetime import datetime, timezone
from helper.token_helper import TokenHelper
from models.reset_tokens_table import ResetToken


templates = Jinja2Templates(directory="templates")
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


@user.get("/reset-password", response_class=HTMLResponse)
async def reset_password_form(request: Request, token: str):
    with SessionLocal() as db:
        token_entry = db.query(ResetToken).filter(ResetToken.token == token).first()
        if not token_entry:
            raise HTTPException(status_code=400, detail="Invalid reset token.")

        current_time = datetime.now(timezone.utc)
        print(
            f"Checking token existence: Current time {current_time}, Expires {token_entry.expires}"
        )

    return templates.TemplateResponse(
        "reset_password.html", {"request": request, "token": token}
    )


@user.post("/user/forgot_password")
async def forgot_password(email: str, request: Request):
    return await UserController.forgot_password(email, request)


@user.post("/reset-password")
async def reset_password_post(token: str = Form(...), new_password: str = Form(...)):
    return await UserController.reset_password(token, new_password)


@user.put("/user")
async def user_update(user: user_dependency, user_update: UserUpdateModel):
    return UserController.user_update(user, user_update)
