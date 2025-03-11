from pydantic import BaseModel, Field


class PasswordChangeModel(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8)
