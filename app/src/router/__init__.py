# --------------------------------------------------------------------------
# Backend Application과 router을 연결하는 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from fastapi import APIRouter

from .router import kakao_router

router = APIRouter(prefix="/kakao-channel/v1")

router.include_router(kakao_router, tags=["kakao-weather-api"])
