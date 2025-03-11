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
