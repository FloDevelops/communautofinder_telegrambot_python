from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean

from .database import Base

class User(Base):
    __tablename__ = 'users'

    telegram_user_id = Column(String, primary_key=True, index=True)
    telegram_username = Column(String)
    telegram_first_name = Column(String)
    telegram_last_name = Column(String)
    telegram_language_code = Column(String)
    telegram_chat_id = Column(String)
    is_enabled = Column(Boolean, default=False)
    has_accepted_communications = Column(Boolean, default=False)
    preferred_city_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated_at = Column(DateTime, default=datetime.utcnow)
