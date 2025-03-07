from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

from sqlalchemy import Enum


class UserModel(BaseModel):
    id: int
    email: str
    name: str
    role: str


class TokenModel(UserModel):
    access_token: str
    token_type: Optional[str] = "Bearer"
