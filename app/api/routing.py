# TODO: make Kakao Bot channel skills and link it.
from fastapi import APIRouter, HTTPException, Depends, Request

from dotenv import load_dotenv

from sqlalchemy.orm import Session

from apps.converter import WeatherForecastTrimmer

from db import crud, schemas
from db.database import SessionLocal

import os
import requests
import json


load_dotenv()

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_weather_data(request_data):
    city_name = request_data.get("city_name")
    api_key = request_data.get("api_key")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=kr"

    # try:
    #     response = requests.get(url, params=request_data)

    #     if response.json().get('cod') != 200:
    #         message = "Error! Cannot get Weather Data."

    #         return {"detail" : message}

    #     return get_ultimate_weather_data(json_response=response.json())

    # except:
    #     message = "Unknown Server Error has occurred!, please contact ME (bbbong9@gmail.com)"

    #     return {"detail" : message}
    response = requests.get(url, params=request_data)

    if response.json().get("cod") != 200:
        message = "날씨 정보를 받아오는데 실패했습니다ㅠㅠ"

        return {"detail": message}

    message = WeatherForecastTrimmer(response.json()).weather_trimmed_data_json
    message["city_name"] = city_name

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

    return {"detail": message}


@router.get("/")
def get_test_response():
    response = "this is test api"

    return response


@router.post("/")
def post_test_response():
    response = {
        "version": "2.0",
        "template": {"outputs": [{"simpleText": {"text": "테스트 택스트 입니다."}}]},
    }

    return response


@router.post("/get-daily-forecast")
async def get_daily_forecast(request: Request, db: Session = Depends(get_db)):
    # the end point router which kakao bot's skill uses.

    # example of Kakao Channel request parameter.
    # {
    # "intent": {
    #     "id": "g7l4sowfugsnagh6q07sm644",
    #     "name": "블록 이름"
    # },
    # "userRequest": {
    #     "timezone": "Asia/Seoul",
    #     "params": {
    #     "ignoreMe": "true"
    #     },
    #     "block": {
    #     "id": "g7l4sowfugsnagh6q07sm644",
    #     "name": "블록 이름"
    #     },
    #     "utterance": "발화 내용",
    #     "lang": null,
    #     "user": {
    #     "id": "932269",
    #     "type": "accountId",
    #     "properties": {}
    #     }
    # },
    # "bot": {
    #     "id": "62fb6c0370055f434dcd360f",
    #     "name": "봇 이름"
    # },
    # "action": {
    #     "name": "pr57lo7x4x",
    #     "clientExtra": null,
    #     "params": {},
    #     "id": "jnew04s5mc9xk3lf5yd1a0bx",
    #     "detailParams": {}
    #   }
    # }

    api_key = os.getenv("WEATHER_API_KEY")

    request_data = await request.json()

    user_name = request_data.get("userRequest").get("user").get("id")

    db_user = crud.get_kakao_user(db, user_name=user_name)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Exists.")

    # default location set to Seoul when user_location is not defined.
    request_data = {"api_key": api_key, "city_name": db_user.user_location}

    response = get_weather_data(request_data)

    return response


@router.post("/edit-user-location", response_model=schemas.KakaoUser)
async def edit_user_info(request: Request, db: Session = Depends(get_db)):
    # the end point router which kakao bot's skill uses.
    # change forecasting location via message.
    request_data = await request.json()

    user_name = request_data.get("userRequest").get("user").get("id")

    db_user = crud.get_kakao_user(db, user_name=user_name)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Exists.")

    user_location = request_data.get("action").get("params").get("user_location")
    user = schemas.KakaoUserLocation(user_name=user_name, user_location=user_location)

    return crud.edit_user_location(db=db, data=user)


@router.post("/edit-user-time", response_model=schemas.KakaoUser)
async def edit_user_time(request: Request, db: Session = Depends(get_db)):
    # the end point router which kakao bot's skill uses.
    # change forecasting time via message.
    request_data = await request.json()

    user_name = request_data.get("userRequest").get("user").get("id")

    db_user = crud.get_kakao_user(db, user_name=user_name)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Exists.")

    user_time_params = request_data.get("action").get("params").get("user_time")
    user_time_json = json.loads(user_time_params)
    user_time = user_time_json.get("time")
    user = schemas.KakaoUserTime(user_name=user_name, user_time=user_time)

    return crud.edit_user_time(db=db, data=user)


@router.post("/create-kakao-user", response_model=schemas.KakaoUser)
async def create_kakao_user(request: Request, db: Session = Depends(get_db)):
    request_data = await request.json()

    user_name = request_data.get("userRequest").get("user").get("id")

    db_user = crud.get_kakao_user(db, user_name=user_name)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists.")

    user_location = request_data.get("action").get("params").get("user_location")
    user_time_params = request_data.get("action").get("params").get("user_time")

    user_time_json = json.loads(user_time_params)
    user_time = user_time_json.get("time")

    user = schemas.KakaoUser(
        user_name=user_name, user_location=user_location, user_time=user_time
    )
    return crud.create_kakao_user(db=db, data=user)


@router.post("/check-city")
async def check_city(request: Request):
    request_data = await request.json()

    return


@router.post("/check-time")
async def check_time(request: Request):
    request_data = await request.json()

    return


@router.get("/get-kakao-user", response_model=schemas.KakaoUser)
def get_kakao_user(user: schemas.KakaoGetUser, db: Session = Depends(get_db)):
    db_user = crud.get_kakao_user(db, user_name=user.user_name)

    return db_user


@router.get("/get-kakao-users")
def get_kakao_users(db: Session = Depends(get_db)):
    return crud.get_kakao_users(db)


@router.delete("/delete-kakao-user")
def delete_kakao_user(user: schemas.KakaoGetUser, db: Session = Depends(get_db)):
    db_user = crud.get_kakao_user(db, user_name=user.user_name)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Exists.")

    return crud.delete_kakao_user(db=db, data=db_user)
