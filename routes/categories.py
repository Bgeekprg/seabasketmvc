# Importing libraries
from typing import Annotated
from fastapi import APIRouter, Depends
from controllers.category_controller import CategoryController
from controllers.auth_controller import AuthController
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from dtos.auth_models import UserModel
from dtos.categories_models import CategoryCreate, CategoryUpdate
from helper.token_helper import TokenHelper

# Declaring router
category = APIRouter(tags=["Categories"])

user_dependency = Annotated[UserModel, Depends(TokenHelper.get_current_user)]


@category.get("/categories")
async def get_categories(id: int = None, status: bool = None):
    return CategoryController.get_categories(id, status)


@category.post("/categories")
async def create_categories(categories: CategoryCreate, user: user_dependency):
    return CategoryController.create_category(categories, user)


@category.put("/categories/{category_id}")
async def update_categories(
    category_id: int, categories: CategoryUpdate, user: user_dependency
):
    return CategoryController.update_category(category_id, categories, user)


@category.delete("/categories/{category_id}")
async def delete_categories(category_id: int, user: user_dependency):
    return CategoryController.delete_category(category_id, user)
