# Importing Libraries
from pydantic import BaseModel
from typing import Any, Optional


# Initializing
class BaseResponseModel(BaseModel):
    data: Any
    message: Optional[str] = None

    class Config:
        from_attributes = True


class BaseErrorModel(BaseModel):
    error: Optional[str] = None

    class Config:
        from_attributes = True
