from datetime import datetime
from typing import Union
from pydantic import BaseModel

class UserBase(BaseModel):
    telegram_user_id: str
    telegram_username: str
    telegram_first_name: str
    telegram_last_name: str
    telegram_language_code: str
    telegram_chat_id: str
    
class UserCreate(UserBase):
    has_accepted_communications: Union[bool, None] = False
    preferred_city_id: str

class UserUpdate(UserBase):
    user_id: bytes
    is_enabled: Union[bool, None]
    has_accepted_communications: Union[bool, None]
    preferred_city_id: str

class User(UserBase):
    user_id: bytes
    telegram_username: str
    telegram_first_name: str
    telegram_last_name: str
    telegram_language_code: str
    telegram_chat_id: str
    is_enabled: bool
    has_accepted_communications: bool
    preferred_city_id: str
    created_at: datetime
    last_updated_at: datetime

    class Config:
        from_attributes = True