import json
from uuid import uuid4

from sqlalchemy import insert, update, delete
from sqlalchemy.orm import Session

from back_reservauto.models.users import models, schemas


def read_users(db: Session):
    return db.query(models.User).all()

def read_user(telegram_user_id: str, db: Session):
    return db.query(models.User).filter(models.User.telegram_user_id == telegram_user_id).first()

def create_user(user: schemas.UserCreate, db: Session):
    db_user = models.User(
        user_id=uuid4().bytes,
        telegram_user_id=user.telegram_user_id,
        telegram_username=user.telegram_username,
        telegram_first_name=user.telegram_first_name,
        telegram_last_name=user.telegram_last_name,
        telegram_language_code=user.telegram_language_code,
        telegram_chat_id=user.telegram_chat_id,
        has_accepted_communications=user.has_accepted_communications,
        preferred_city_id=user.preferred_city_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(user: schemas.UserUpdate, db: Session):
    statement = (
        update(models.User)
        .where(models.User.telegram_user_id == user.telegram_user_id)
        .values(
            telegram_username=user.telegram_username,
            telegram_first_name=user.telegram_first_name,
            telegram_last_name=user.telegram_last_name,
            telegram_language_code=user.telegram_language_code,
            telegram_chat_id=user.telegram_chat_id,
            is_enabled=user.is_enabled,
            has_accepted_communications=user.has_accepted_communications,
            preferred_city_id=user.preferred_city_id,
        )
    )
    db.execute(statement)
    db.commit()
    return user


def delete_user(telegram_user_id: str, db: Session):
    statement = (
        delete(models.User)
        .where(models.User.telegram_user_id == telegram_user_id)
    )
    db.execute(statement)
    db.commit()
    return True