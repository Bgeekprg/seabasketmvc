# Loading the .env file
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from os.path import join, dirname
from config.db_config import *
from fastapi.staticfiles import StaticFiles
from helper.api_helper import APIHelper
from helper.cors_helper import CORSHelper
from helper.logger_helper import setup_logger
from sqlalchemy.exc import OperationalError

# Setting up dotenv
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Importing libraries
from fastapi import FastAPI, Request
from routes.auth import auth
from routes.categories import category
from routes.products import product
from routes.users import user
from routes.carts import cart
from routes.orders import order
from routes.review_ratings import review_rating
from fastapi.exceptions import RequestValidationError

import i18n

# Setup Logger
setup_logger()


# Setup i18n
i18n.load_path.append("language/")
i18n.set("filename_format", "{namespace}.{locale}.{format}")
i18n.set("file_format", "json")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with engine.connect() as conn:
            pass
        print("✅ DB connected")
    except OperationalError as e:
        print("❌ DB connection failed:", e)

    yield

    engine.dispose()
    print("🔌 DB disconnected")


# Initializing app
app = FastAPI(
    title="SeaBasket",
    lifespan=lifespan,
    # version="0.1.0",
)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
# Setup CORS
CORSHelper.setup_cors(app)


# Request validation error
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if exc.errors()[0]["type"] == "value_error":
        return APIHelper.send_error_response(
            errorMessageKey=f"{exc.errors()[0]['msg']}"
        )
    else:
        return APIHelper.send_error_response(
            errorMessageKey=f"{exc.errors()[0]['loc'][1]} {exc.errors()[0]['msg']}"
        )


# Including the routes
app.include_router(auth)
app.include_router(category)
app.include_router(product)
app.include_router(cart)
app.include_router(user)
app.include_router(order)
app.include_router(review_rating)
