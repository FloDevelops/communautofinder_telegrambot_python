from sqlalchemy.orm import Session

from back_reservauto.models.users import models, schemas

def read_users(db: Session):
    return db.query(models.User).all()

def read_user(user_id: str, db: Session):
    return db.query(models.User).filter(models.User.telegram_user_id == user_id).first()

def create_user(user: schemas.UserCreate, db: Session):
    db_user = models.User(
        telegram_user_id=user.telegram_user_id,
        telegram_username=user.telegram_username,
        telegram_first_name=user.telegram_first_name,
        telegram_last_name=user.telegram_last_name,
        telegram_language_code=user.telegram_language_code,
        telegram_chat_id=user.telegram_chat_id,
        is_enabled=user.is_enabled,
        has_accepted_communications=user.has_accepted_communications,
        preferred_city_id=user.preferred_city_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(user: schemas.UserUpdate, db: Session):
    db_user = db.query(models.User).filter(models.User.telegram_user_id == user.telegram_user_id).first()
    if db_user is None:
        return None
    db_user.telegram_username = user.telegram_username
    db_user.telegram_first_name = user.telegram_first_name
    db_user.telegram_last_name = user.telegram_last_name
    db_user.telegram_language_code = user.telegram_language_code
    db_user.telegram_chat_id = user.telegram_chat_id
    db_user.is_enabled = user.is_enabled
    db_user.has_accepted_communications = user.has_accepted_communications
    db_user.preferred_city_id = user.preferred_city_id
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(user_id: str, db: Session):
    db_user = db.query(models.User).filter(models.User.telegram_user_id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user