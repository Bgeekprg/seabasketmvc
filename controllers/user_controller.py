from datetime import datetime, timedelta, timezone
import logging
import os
import secrets
from fastapi import HTTPException, Request, status
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
import i18n
from config.db_config import SessionLocal
from dtos.auth_models import UserModel
from dtos.password_models import PasswordChangeModel
from dtos.user_models import UserResponseModel
from helper.admin_helper import ADMINHelper
from helper.api_helper import APIHelper
from helper.hashing import Hash
from models.reset_tokens_table import ResetToken
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

    async def forgot_password(email: str, request: Request):
        mail_username = os.getenv("EMAIL_HOST_USER")
        mail_password = os.getenv("EMAIL_HOST_PASSWORD")

        if not mail_username or not mail_password:
            logging.error("Email credentials are missing.")
            raise HTTPException(
                status_code=500, detail="Email credentials are missing."
            )

        conf = ConnectionConfig(
            MAIL_USERNAME=mail_username,
            MAIL_PASSWORD=mail_password,
            MAIL_FROM="userfastapi@gmail.com",
            MAIL_PORT=2525,
            MAIL_SERVER="sandbox.smtp.mailtrap.io",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
        )

        with SessionLocal() as db:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                return APIHelper.send_error_response(
                    errorMessageKey="translations.USER_NOT_FOUND"
                )

            reset_token = secrets.token_urlsafe(32)
            # Ensure timezone-aware datetime
            expires = datetime.now(timezone.utc) + timedelta(hours=3)

            token_entry = ResetToken(token=reset_token, email=email, expires=expires)
            db.add(token_entry)
            db.commit()

        reset_link = f"{request.base_url}reset-password/?token={reset_token}"
        html_content = f"Click the following link to reset your password:<a href='{reset_link}'>Reset Password</a>"

        message = MessageSchema(
            subject="Password Reset Request",
            recipients=[email],
            body=html_content,
            subtype="html",
        )

        fm = FastMail(conf)

        try:
            await fm.send_message(message)
            logging.info(f"Password reset email sent to {email}")
            return {"message": "Password reset email sent successfully"}
        except Exception as e:
            logging.error(f"Error sending email: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to send password reset email."
            )

    async def reset_password(token: str, new_password: str):
        with SessionLocal() as db:
            token_entry = db.query(ResetToken).filter(ResetToken.token == token).first()
            if not token_entry:
                raise HTTPException(
                    status_code=400, detail="Invalid or expired reset token."
                )

            current_time = datetime.now(timezone.utc)
            # Ensure expires is timezone-aware; if database stored it as naive, make it UTC
            expires_aware = token_entry.expires
            if expires_aware.tzinfo is None:
                expires_aware = expires_aware.replace(tzinfo=timezone.utc)

            if current_time > expires_aware:
                db.delete(token_entry)
                db.commit()
                raise HTTPException(status_code=400, detail="Reset token has expired.")

            if len(new_password) < 8:
                raise HTTPException(
                    status_code=400, detail="Password must be at least 8 characters."
                )

            user = db.query(User).filter(User.email == token_entry.email).first()
            if not user:
                db.delete(token_entry)
                db.commit()
                raise HTTPException(
                    status_code=400, detail=i18n.t("translations.USER_NOT_FOUND")
                )

            user.password = Hash.get_hash(new_password)
            db.delete(token_entry)
            db.commit()

        return APIHelper.send_success_response(
            successMessageKey="translations.PASSWORD_RESET_SUCCESS"
        )
