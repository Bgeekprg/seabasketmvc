import locale
from fastapi import HTTPException
import i18n

from dtos.auth_models import UserModel
from helper.api_helper import APIHelper


class ADMINHelper:
    def isAdmin(user: UserModel):
        if user.role == "admin":
            return True
        raise HTTPException(
            status_code=403,
            detail=i18n.t(key="translations.PERMISSION_DENIED", locale=locale),
        )
