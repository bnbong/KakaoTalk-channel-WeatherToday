from sqlalchemy import Column, Integer, String
from .database import Base


class KakaoChannelUser(Base):
    __tablename__ = "kakao_channel_users"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))

    user_time = Column(String(50), default="0500")
    user_location_first = Column(String(50))
    user_location_second = Column(String(50), nullable=True)
    user_location_third = Column(String(50), nullable=True)
