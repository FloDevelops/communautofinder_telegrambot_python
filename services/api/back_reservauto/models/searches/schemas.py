from datetime import datetime
from pydantic import BaseModel

class SearchBase(BaseModel):
    user_id: bytes
    search_type: str
    city_id: str
    area_min_lat: float
    area_max_lat: float
    area_min_lon: float
    area_max_lon: float
    start_date: datetime
    end_date: datetime
    
class SearchCreate(SearchBase):
    pass

class SearchUpdate(SearchBase):
    search_status: str

class Search(SearchBase):
    search_id: bytes
    search_status: str
    created_at: datetime
    last_updated_at: datetime

    class ConfigDict:
        from_attributes = True
