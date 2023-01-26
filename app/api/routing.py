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
    city_name = request_data.get('city_name')
    api_key = request_data.get('api_key')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=kr'


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

    if response.json().get('cod') != 200:
        message = "Error! Cannot get Weather Data."

        return {"detail" : message}

    return get_ultimate_weather_data(json_response=response.json())

def get_ultimate_weather_data(json_response):
    #TODO: edit this code.
    message = WeatherForecastTrimmer(json_response).weather_trimmed_data_json

    return message

@router.get('/')
def get_test_response():
    response = 'this is test api'

    return response

@router.post('/')
def post_test_response():
    response = 'this is test post api'

    return response

@router.post('/get-daily-forecast')
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

    api_key = os.getenv('WEATHER_API_KEY')

    request_data = await request.json()

    user_name = request_data.get('action').get('params').get('user_name')

    db_user = crud.get_kakao_user(db, user_name=user_name)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Exists.")

    # user_preferred_time = db_user.user_time # code goes here.
    # user_preferred_time = str(user_preferred_time) # 유저가 원하는 알람 시간이므로 API param에 포함되지 않는다. 나중에 skill관련으로 제공될예정.

    # API 제공 시간은 각 base time values += 10분

    # default location set to Seoul when user_location is not defined.
    request_data = {
        'api_key' : api_key,
        'city_name' : db_user.user_location
    }

    response = get_weather_data(request_data)
    
    return response

@router.post('/edit-user-location', response_model=schemas.KakaoUser)
def edit_user_info(user: schemas.KakaoGetUser, db: Session = Depends(get_db)):
    # the end point router which kakao bot's skill uses.
    # change forecasting location via message.
    db_user = crud.get_kakao_user(db, user_name=user.user_name)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Exists.")
    
    return crud.edit_user_location(db=db, data=user)

@router.post('/edit-user-time', response_model=schemas.KakaoUser)
def edit_user_time(user: schemas.KakaoUserTime, db: Session = Depends(get_db)):
    # the end point router which kakao bot's skill uses.
    # change forecasting time via message.
    db_user = crud.get_kakao_user(db, user_name=user.user_name)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Exists.")

    return crud.edit_user_time(db=db, data=user)

@router.post('/create-kakao-user', response_model=schemas.KakaoUser)
async def create_kakao_user(request: Request, db: Session = Depends(get_db)):
    # db_user = crud.get_kakao_user(db, user_name=user.user_name)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="User already exists.")
    request_data = await request.json()

    user_name = request_data.get('userRequest').get('user').get('id')

    db_user = crud.get_kakao_user(db, user_name=user_name)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists.")
    
    user_location = request_data.get('action').get('params').get('user_location')
    user_time_params = request_data.get('action').get('params').get('user_time')

    user_time_json = json.loads(user_time_params)
    user_time = user_time_json.get('time')

    user = schemas.KakaoUser(user_name=user_name, user_location=user_location, user_time=user_time)
    return crud.create_kakao_user(db=db, data=user)

@router.post('/check-city')
async def check_city(request: Request):
    request_data = await request.json()

    return 

@router.get('/get-kakao-user', response_model=schemas.KakaoUser)
def get_kakao_user(user: schemas.KakaoGetUser, db: Session = Depends(get_db)):
    db_user = crud.get_kakao_user(db, user_name=user.user_name)

    return db_user

@router.get('/get-kakao-users')
def get_kakao_users(db: Session = Depends(get_db)):
    
    return crud.get_kakao_users(db)

@router.delete('/delete-kakao-user')
def delete_kakao_user(user: schemas.KakaoGetUser, db: Session = Depends(get_db)):
    db_user = crud.get_kakao_user(db, user_name=user.user_name)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Exists.")

    return crud.delete_kakao_user(db=db, data=db_user)