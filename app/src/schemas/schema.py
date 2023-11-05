# --------------------------------------------------------------------------
# KakaoChannelUser model의 schema를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.db.models import KakaoChannelUser


class KakaoUserBase(BaseModel):
    user_name: str = Field(
        ...,
        title="유저의 카카오톡 닉네임",
        description="유저의 카카오톡 닉네임을 입력합니다.",
    )
    user_time: Optional[str] = Field(
        "0800",
        title="유저가 기상 예보를 받아보기 원하는 시간",
        description="유저가 기상 예보를 받아보기 원하는 시간을 입력합니다. 입력하지 않으면 기본값인 08시로 설정됩니다.",
    )
    user_location: Optional[str] = Field(
        "서울특별시",
        title="유저가 기상 예보를 선호하는 위치",
        description="설정되어 있는 user_location 값을 바탕으로 기상 예보 데이터를 받아옵니다.",
    )
    is_active: bool = Field(
        ...,
        title="유저의 활성화 여부",
        description="유저 계정의 활성화 여부를 boolean 값으로 나타냅니다.",
    )


class KakaoUser(KakaoUserBase):
    uid: UUID = Field(
        ...,
        title="유저의 고유 식별자",
        description="유저의 고유 식별자를 나타냅니다.",
    )

    class ConfigDict:
        schema_extra = {
            "example": {
                "uid": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "user_name": "김철수",
                "user_time": "0800",
                "user_location": "서울특별시",
                "is_active": True,
            }
        }
        orm_model = KakaoChannelUser
        from_attributes = True


class KakaoUserCreate(KakaoUserBase):
    pass


class KakaoUserUpdate(KakaoUserBase):
    user_name: Optional[str] = Field(
        None,
        title="유저의 카카오톡 닉네임",
        description="유저의 카카오톡 닉네임을 입력합니다.",
    )
    user_time: Optional[str] = Field(
        "0800",
        title="유저가 기상 예보를 받아보기 원하는 시간",
        description="유저가 기상 예보를 받아보기 원하는 시간을 입력합니다. 입력하지 않으면 기본값인 08시로 설정됩니다.",
    )
    user_location: Optional[str] = Field(
        "서울특별시",
        title="유저가 기상 예보를 선호하는 위치",
        description="설정되어 있는 user_location 값을 바탕으로 기상 예보 데이터를 받아옵니다.",
    )
    is_active: Optional[bool] = Field(
        True,
        title="유저의 활성화 여부",
        description="유저 계정의 활성화 여부를 boolean 값으로 나타냅니다.",
    )
