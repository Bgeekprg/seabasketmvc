# Importing libraries
from fastapi import APIRouter, Depends
from controllers.auth_controller import AuthController
from fastapi.security import OAuth2PasswordRequestForm
from dtos.user_models import CreateUserModel

# Declaring router
auth = APIRouter(tags=["Authentication"])

@auth.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends()):
    return AuthController.login(request)

@auth.post('/register')
async def register(user_data: CreateUserModel):
    return AuthController.register(user_data)
