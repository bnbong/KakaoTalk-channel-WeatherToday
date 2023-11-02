# TODO: return type 명시
# --------------------------------------------------------------------------
# KakaoChannelUser model의 CRUD를 담당하는 메서드를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import aiohttp

from fastapi import Request, HTTPException
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import KakaoChannelUser
from src.schemas import schema
from src.utils.converter import WeatherForecastTrimmer


async def get_weather_data(request: Request):
    # TODO: city_name, app_key 부분 수정.
    """
        {
            "detail": {
                "현재 날씨": "Clear",
                "날씨 상세": "맑음",
                "현재 온도": "-7 도",
                "체감 온도": "-12 도",
                "최고 온도(현재 시각으로부터 전후 3시간)": "-5 도",
                "최저 온도(현재 시각으로부터 전후 3시간)": "-9 도",
                "가시 거리": "10000 미터",
                "풍속": "초속 3.09 미터",
                "구름 낀 정도(백분율)": "0%",
                "일출 시간": "07시 39분 45초",
                "일몰 시간": "17시 49분 17초",
                "도시 이름": "과천시"
            }
        }
            --->
        {
        "detail": {
            "weather_info": "Clear",
            "weather_detail": "맑음",
            "temperature": "-7 도",
            "feeling_temperature": "-12 도",
            "high_temperature": "-5 도",
            "low_temperature": "-9 도",
            "visibility": "10000 미터",
            "wind_speed": "초속 3.09 미터",
            "cloud_percentage": "0%",
            "sunrise_time": "07시 39분 45초",
            "sunset_time": "17시 49분 17초",
            "city_name": "과천시"
        }
    }
    """
    city_name = request.get("city_name")
    api_key = request.get("api_key")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=kr"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                message = "날씨 정보를 받아오는데 실패했습니다ㅠㅠ"
                raise HTTPException(status_code=400, detail=message)

            data = await response.json()
            message = WeatherForecastTrimmer(data).weather_trimmed_data_json
            message["city_name"] = city_name

            return {"detail": message}


async def get_kakao_user(db: AsyncSession, user_uid: UUID):
    response_model = schema.KakaoUser
    query = select(KakaoChannelUser).filter(KakaoChannelUser.uid == user_uid)

    result = (await db.execute(query)).scalar_one_or_none()
    return response_model.model_validate(result.__dict__)


async def create_kakao_user(db: AsyncSession, user: schema.KakaoUserBase):
    response_model = schema.KakaoUser
    user_data = user.model_dump()
    db_user = KakaoChannelUser(**user_data)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return response_model.model_validate(db_user.__dict__)


async def edit_kakao_user(
    db: AsyncSession, user_uid: UUID, user: schema.KakaoUserUpdate
):
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


async def delete_kakao_user(db: AsyncSession, user_uid: UUID):
    query = select(KakaoChannelUser).filter(KakaoChannelUser.uid == user_uid)
    db_user = (await db.execute(query)).scalar_one_or_none()
    if db_user:
        await db.delete(db_user)
        await db.commit()
    else:
        return None
    return user_uid
