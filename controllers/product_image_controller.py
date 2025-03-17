import os
from typing import List
from uuid import uuid4
from fastapi import UploadFile
from config.db_config import SessionLocal
from dtos.auth_models import UserModel
from helper.admin_helper import ADMINHelper
from models.product_images_table import ProductImage


class ProductImageController:
    UPLOAD_FOLDER = "uploads/product_images"

    def _save_image(image: UploadFile):
        os.makedirs(ProductImageController.UPLOAD_FOLDER, exist_ok=True)
        file_extension = image.filename.split(".")[-1]
        file_name = f"{uuid4()}.{file_extension}"
        file_path = os.path.join(ProductImageController.UPLOAD_FOLDER, file_name)

        with open(file_path, "wb") as buffer:
            buffer.write(image.file.read())

        return file_path

    async def upload_product_images(
        user: UserModel, product_id: int, files: List[UploadFile]
    ):
        if ADMINHelper.isAdmin(user):
            pass

        uploaded_image = files[0]

        file_path = ProductImageController._save_image(uploaded_image)

        image_url = (
            f"/{ProductImageController.UPLOAD_FOLDER}/{os.path.basename(file_path)}"
        )

        with SessionLocal() as db:
            db_image = ProductImage(productId=product_id, imageUrl=image_url)
            db.add(db_image)
            db.commit()
            db.refresh(db_image)

        return {"message": "Image uploaded successfully", "image": db_image}
