from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, BINARY, TypeDecorator, LargeBinary
from sqlalchemy.orm import relationship

from back_reservauto.database import Base
from back_reservauto.dependencies import ByteArrayString

class User(Base):
    __tablename__ = 'users'

    user_id = Column(ByteArrayString(16), primary_key=True)
    telegram_user_id = Column(String, unique=True)
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
    # searches = relationship('Search', back_populates='telegram_user_id')
