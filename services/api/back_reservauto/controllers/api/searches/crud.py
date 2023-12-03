from typing import Union
from uuid import uuid4

from sqlalchemy import insert, update, delete
from sqlalchemy.orm import Session

from back_reservauto.models.searches import models, schemas

def create_search(search: schemas.SearchCreate, db: Session) -> dict:
    db_search = models.Search(
        search_id=uuid4().bytes,
        user_id=search.user_id,
        search_type=search.search_type,
        city_id=search.city_id,
        area_min_lat=search.area_min_lat,
        area_max_lat=search.area_max_lat,
        area_min_lon=search.area_min_lon,
        area_max_lon=search.area_max_lon,
        start_date=search.start_date,
        end_date=search.end_date,
    )
    db.add(db_search)
    db.commit()
    db.refresh(db_search)
    return db_search

def read_searches(telegram_user_id: str, db: Session) -> Union[list, None]:
    telegram_user_id = str(telegram_user_id)
    searches = db.query(models.Search).filter(models.Search.telegram_user_id == str(telegram_user_id)).all()
    return searches

def read_search(search_id: str, db: Session) -> dict:
    search = db.query(models.Search).filter(models.Search.search_id == search_id).first()
    return search

def update_search(search_id: str, search: schemas.SearchUpdate, db: Session) -> dict:
    db_search = db.query(models.Search).filter(models.Search.search_id == search_id).first()
    if db_search is None:
        return None
    db_search.telegram_user_id = search.telegram_user_id
    db_search.search_type = search.search_type
    db_search.city_id = search.city_id
    db_search.area_min_lat = search.area_min_lat
    db_search.area_max_lat = search.area_max_lat
    db_search.area_min_lon = search.area_min_lon
    db_search.area_max_lon = search.area_max_lon
    db_search.start_date = search.start_date
    db_search.end_date = search.end_date
    db_search.search_status = search.search_status
    db.commit()
    db.refresh(db_search)
    return db_search

def delete_search(search_id: str, db: Session) -> dict:
    db_search = db.query(models.Search).filter(models.Search.search_id == search_id).first()
    if db_search is None:
        return None
    db.delete(db_search)
    db.commit()
    return db_search
