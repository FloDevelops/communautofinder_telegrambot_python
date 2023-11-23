from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from back_reservauto.dependencies import get_db
from back_reservauto.models.searches import schemas
from . import crud


router = APIRouter(
    prefix='/searches',
    tags=['searches']
)

@router.get('')
def read_searches(telegram_user_id: str, db: Session = Depends(get_db)):
    searches = crud.read_searches(telegram_user_id, db)
    return searches

@router.get('/{search_id}')
def read_search(search_id: str, telegram_user_id: str, db: Session = Depends(get_db)):
    db_search = crud.read_search(search_id, telegram_user_id, db)
    if db_search is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Search not found')
    return db_search

@router.post('')
def create_search(search: schemas.SearchCreate, db: Session = Depends(get_db)):
    db_search = crud.create_search(search, db)
    return db_search

@router.put('/{search_id}')
def update_search(search_id: str, search: schemas.SearchUpdate, db: Session = Depends(get_db)):
    db_search = crud.read_search(search_id, search.telegram_user_id, db)
    if db_search is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Search not found')
    return crud.update_search(search_id, search, db)

@router.delete('/{search_id}')
def delete_search(search_id: str, db: Session = Depends(get_db)):
    db_search = crud.delete_search(search_id, db)
    if db_search is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Search not found')
    return db_search
