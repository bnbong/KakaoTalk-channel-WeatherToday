# --------------------------------------------------------------------------
# KakaoChannelUser model의 CRUD를 담당하는 메서드를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import requests

from typing import Optional, Union, Any

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import KakaoChannelUser
from src.schemas import schema
from src.utils.converter import WeatherForecastTrimmer


def get_weather_data(request_data) -> Optional[list]:
    url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

    response = requests.get(url, params=request_data)

    return get_ultimate_weather_data(json_response=response.json())


def get_ultimate_weather_data(json_response) -> Union[Optional[list], tuple[Any, str]]:
    response_header = json_response.get("response").get("header")

    if response_header.get("resultCode") != "00":
        if response_header.get("resultMsg") == "NO_DATA":
            return json_response.json(), "We got wrong request values :("

    else:
        json_response = (
            json_response.get("response").get("body").get("items").get("item")
        )

        message = []

        for item in json_response:
            item_pointer = WeatherForecastTrimmer()
            item_pointer.category_converter(item)

            if item_pointer.weather_value is not None:
                message.append(item_pointer.weather_value)

        return message


async def get_kakao_user(db: AsyncSession, user_uid: UUID) -> schema.KakaoUser:
    response_model = schema.KakaoUser
    query = select(KakaoChannelUser).filter(KakaoChannelUser.uid == user_uid)

    result = (await db.execute(query)).scalar_one_or_none()
    return response_model.model_validate(result.__dict__)


async def create_kakao_user(
    db: AsyncSession, user: schema.KakaoUserBase
) -> schema.KakaoUser:
    response_model = schema.KakaoUser
    user_data = user.model_dump()
    db_user = KakaoChannelUser(**user_data)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return response_model.model_validate(db_user.__dict__)


async def edit_kakao_user(
    db: AsyncSession, user_uid: UUID, user: schema.KakaoUserUpdate
) -> schema.KakaoUser:
    response_model = schema.KakaoUser
    query = select(KakaoChannelUser).filter(KakaoChannelUser.uid == user_uid)
    db_user = (await db.execute(query)).scalar_one_or_none()
    if db_user is None:
        return None
    update_data = user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return response_model.model_validate(db_user.__dict__)


async def delete_kakao_user(db: AsyncSession, user_uid: UUID) -> Optional[UUID]:
    query = select(KakaoChannelUser).filter(KakaoChannelUser.uid == user_uid)
    db_user = (await db.execute(query)).scalar_one_or_none()
    if db_user:
        await db.delete(db_user)
        await db.commit()
    else:
        return None
    return user_uid
