# --------------------------------------------------------------------------
# KakaoChannelUser model의 API router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from logging import getLogger
from uuid import UUID
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import database
from src.db.database import settings
from src.schemas import schema
from src.crud import weather_crud as crud
from src.utils.xlsx_reader import XlsxReader

log = getLogger(__name__)

kakao_router = APIRouter()


@kakao_router.get("/_ping")
async def ping():
    return {"message": "pong!"}


@kakao_router.get("/user/{user_uid}", response_model=schema.KakaoUser)
async def get_kakao_user(user_uid: UUID, db: AsyncSession = Depends(database.get_db)):
    user = await crud.get_kakao_user(db=db, user_uid=user_uid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@kakao_router.post("/user/", response_model=schema.KakaoUser)
async def create_kakao_user(
    user: schema.KakaoUserBase, db: AsyncSession = Depends(database.get_db)
):
    return await crud.create_kakao_user(db=db, user=user)


@kakao_router.post("/daily-forecast")
async def get_daily_forecast_endpoint(
    request: Request, db: AsyncSession = Depends(database.get_db)
):
    service_key = settings.WEATHER_API_APP_KEY
    target_date = date.today().__format__("%Y%m%d")
    num_of_rows = "10"

    request_data = await request.json()
    user_name = request_data.get("action").get("params").get("user_name")

    db_user = await crud.get_kakao_user_by_name(db, user_name=user_name)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Exists.")

    nx, ny = XlsxReader().filter_xlsx_data(db_user.user_location)

    # user_preferred_time = db_user.user_time # code goes here.
    # user_preferred_time = str(user_preferred_time) # 유저가 원하는 알람 시간이므로 API param에 포함되지 않는다. 나중에 skill관련으로 제공될예정.

    # base time possible setting values = 0200 0500 0800 1100 1400 1700 2000 2300
    # API 제공 시간은 각 base time values += 10분

    # default location set to Seoul
    request_data = {
        "serviceKey": service_key,
        "numOfRows": num_of_rows,
        "pageNo": "1",
        "dataType": "JSON",
        "base_date": target_date,
        "base_time": "0200",  # base time 중 오늘 날씨까지 제공되는 base time 은 0200 이 유일해보임. (오늘, 내일, 모레 날씨 제공)
        "nx": nx,
        "ny": ny,
    }

    response = crud.get_weather_data(request_data)
    """
        API가 제공하는 날씨 데이터 정보
        value of the key 'item' is list.

        TMN - 일 최저 기온
        TMX - 일 최고 기온
        POP - 강수확률
        PTY - 강수형태
        PCP - 1시간 강수량
        REH - 습도
        WSD - 풍속
        SKY - 하늘상태
        SNO - 적설양
    """

    response = {
        "풍속": response[0],
        "하늘 상태": response[1],
        "강수 확률": response[2],
        "현재 강수 상태": response[3],
    }

    return response


@kakao_router.put("/user/{user_uid}", response_model=schema.KakaoUser)
async def edit_kakao_user(
    user_uid: UUID,
    user: schema.KakaoUserUpdate,
    db: AsyncSession = Depends(database.get_db),
):
    updated_user = await crud.edit_kakao_user(db=db, user_uid=user_uid, user=user)
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return updated_user


@kakao_router.delete("/user/{user_uid}", response_model=UUID)
async def delete_kakao_user(
    user_uid: UUID, db: AsyncSession = Depends(database.get_db)
):
    deleted_user_uid = await crud.delete_kakao_user(db=db, user_uid=user_uid)
    if deleted_user_uid is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return deleted_user_uid
