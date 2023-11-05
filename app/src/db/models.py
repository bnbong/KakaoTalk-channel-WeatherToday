# --------------------------------------------------------------------------
# KakaoChannelUser model을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import uuid

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

from ._base import ModelBase


class KakaoChannelUser(ModelBase):
    uid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    user_name = Column(String(200), unique=True)
    user_time = Column(String(50), default="0800")
    user_location = Column(String(50), default="서울특별시")

    is_active = Column(Boolean, default=True)
