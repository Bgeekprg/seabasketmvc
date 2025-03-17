import re
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
from dtos.auth_models import UserModel

# from helper.validation_helper import ValidationHelper


class CreateUserModel(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: str
    role: str = Field(default="customer")
    status: bool


class UserResponseModel(BaseModel):
    email: EmailStr
    name: str
    role: str
    status: bool


class UserUpdateModel(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    phoneNumber: Optional[str] = None
    profilePic: Optional[str] = None

    @validator("phoneNumber")
    def validate_phone_number(cls, v):
        if v:
            phone_regex = r"^\+?[1-9]\d{1,14}$"
            if not re.match(phone_regex, v):
                raise ValueError("Invalid phone number format")
        return v
