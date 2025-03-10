from fastapi import Depends
from sqlalchemy import select
from config.db_config import SessionLocal, engine
from models.users_table import User
from sqlalchemy.orm import Session


class DBHelper:

    def get_user_by_email(email: str):
        with SessionLocal() as db:
            return db.query(User).filter(User.email == email).first()

    def get_user_by_mobile(phone_number: str):
        with SessionLocal() as db:
            return db.query(User).filter(User.phoneNumber == phone_number).first()

    def get_user_by_id(id: int):
        with SessionLocal() as db:
            return db.query(User).filter(User.id == id).first()
