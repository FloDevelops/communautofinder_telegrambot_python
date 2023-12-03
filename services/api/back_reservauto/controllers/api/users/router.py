from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from back_reservauto.dependencies import get_db
from back_reservauto.models.users import schemas
from . import crud


router = APIRouter(
    prefix='/users',
    tags=['users'],
)

@router.get('')
def read_users(db: Session = Depends(get_db)):
    users = crud.read_users(db)
    return users

@router.get('/{telegram_user_id}')
def read_user(telegram_user_id: str, db: Session = Depends(get_db)):
    db_user = crud.read_user(telegram_user_id, db)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return db_user

@router.post('')
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.read_user(user.telegram_user_id, db)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')
    return crud.create_user(user, db)

@router.put('/{telegram_user_id}')
def update_user(telegram_user_id: str, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.read_user(telegram_user_id, db)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return crud.update_user(user, db)

@router.delete('/{telegram_user_id}')
def delete_user(telegram_user_id: str, db: Session = Depends(get_db)):
    db_user = crud.read_user(telegram_user_id, db)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return crud.delete_user(telegram_user_id, db)

