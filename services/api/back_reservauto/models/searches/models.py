from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Enum, DECIMAL, BINARY
# from sqlalchemy.orm import relationship

from back_reservauto.database import Base

class Search(Base):
    __tablename__ = 'searches'

    search_id = Column(BINARY(16), primary_key=True)
    user_id = Column(BINARY(16))
    search_type = Column(Enum('station','flex', name='search_type'))
    city_id = Column(String)
    area_min_lat = Column(DECIMAL)
    area_max_lat = Column(DECIMAL)
    area_min_lon = Column(DECIMAL)
    area_max_lon = Column(DECIMAL)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    search_status = Column(Enum('pending','running','completed','failed', name='search_status'), default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated_at = Column(DateTime, default=datetime.utcnow)
