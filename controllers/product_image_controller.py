import os
from typing import List
from uuid import uuid4
from fastapi import HTTPException, UploadFile
import i18n
from config.db_config import SessionLocal
from dtos.auth_models import UserModel
from helper.admin_helper import ADMINHelper
from helper.api_helper import APIHelper
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

        image_urls = []
        for uploaded_image in files:
            file_path = ProductImageController._save_image(uploaded_image)

            image_url = (
                f"/{ProductImageController.UPLOAD_FOLDER}/{os.path.basename(file_path)}"
            )
            image_urls.append(image_url)

            with SessionLocal() as db:
                db_image = ProductImage(productId=product_id, imageUrl=image_url)
                db.add(db_image)
                db.commit()
                db.refresh(db_image)

        return APIHelper.send_success_response(
            data=image_urls,
            successMessageKey="translations.PRODUCT_IMAGES_UPLOAD_SUCCESS",
        )

    def get_product_images(product_id: int):
        with SessionLocal() as db:
            db_images = (
                db.query(ProductImage)
                .filter(ProductImage.productId == product_id)
                .all()
            )
            return db_images

    def delete_product_image(product_id: int, image_id: int, user: UserModel):
        if ADMINHelper.isAdmin(user):
            pass
        with SessionLocal() as db:
            db_image = (
                db.query(ProductImage)
                .filter(
                    ProductImage.id == image_id, ProductImage.productId == product_id
                )
                .first()
            )

            if not db_image:
                raise HTTPException(
                    status_code=404,
                    detail=i18n.t(key="translations.PRODUCT_IMAGE_NOT_FOUND"),
                )

            image_path = os.path.join(
                ProductImageController.UPLOAD_FOLDER,
                os.path.basename(db_image.imageUrl),
            )

            if os.path.exists(image_path):
                os.remove(image_path)

            db.delete(db_image)
            db.commit()

            return APIHelper.send_success_response(
                successMessageKey="translations.PRODUCT_IMAGES_DELETE_SUCCESS"
            )
