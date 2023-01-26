from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class KakaoChannelUser(Base):
    __tablename__ = "kakao_channel_users"

    id = Column(Integer, primary_key=True, index=True)
    
    user_name = Column(String(200), unique=True)
    user_time = Column(String(50), default="0800")
    user_location = Column(String(50), default='서울특별시')

    is_active = Column(Boolean, default=True)

