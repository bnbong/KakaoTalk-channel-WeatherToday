from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class KakaoChannelUsers(Base):
    __tablename__ = "kakao_channel_users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer(50))
    user_location_id = Column(Integer, ForeignKey("local_location_xy.id"))
    
    user_selected_location = relationship("LocalLocations")


class LocalLocations(Base):
    __tablename__ = "local_location_xy"

    id = Column(Integer, primary_key=True)
    location_name = Column(String(50))
    nx = Column(Integer(50))
    ny = Column(Integer(50))
