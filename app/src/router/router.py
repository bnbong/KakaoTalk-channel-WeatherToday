# TODO: crud 로직들을 연결하여 라우터 완성.
# --------------------------------------------------------------------------
# KakaoChannelUser model의 API router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from logging import getLogger
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import database
from src.schemas import schema

log = getLogger(__name__)

kakao_router = APIRouter()


@kakao_router.get("/_ping")
async def ping():
    return {"message": "pong!"}


@kakao_router.get("/user/{user_uid}", response_model=schema.KakaoUser)
async def get_kakao_user(user_uid: UUID, db: AsyncSession = Depends(database.get_db)):
    pass


@kakao_router.post("/user", response_model=schema.KakaoUser)
async def create_kakao_user(user: schema.KakaoUserBase, db: AsyncSession = Depends(database.get_db)):
    pass


@kakao_router.post("/daily-forecast")
async def get_daily_forecast(db: AsyncSession = Depends(database.get_db)):
    pass


@kakao_router.put("/user/{user_uid}", response_model=schema.KakaoUser)
async def edit_kakao_user(user_uid: UUID, user: schema.KakaoUserUpdate, db: AsyncSession = Depends(database.get_db)):
    pass


@kakao_router.delete("/user/{user_uid}", response_model=int)
async def delete_kakao_user(
    user_uid: UUID, db: AsyncSession = Depends(database.get_db)
):
    pass
