# TODO: make Kakao Bot channel skills and link it.
from fastapi import APIRouter, HTTPException, Depends, Request

from datetime import date

from dotenv import load_dotenv

from sqlalchemy.orm import Session

from apps.xlsx_reader import XlsxReader
from apps.user_data_trimmer import UserDataTrimmer
from apps.converter import ForecastDataTrimmer

from db import crud, schemas
from db.database import SessionLocal

import os
import requests


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
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    
    response = requests.get(url, params=request_data)

    return get_ultimate_weather_data(json_response=response.json())

def get_ultimate_weather_data(json_response):
    response_header = json_response.get('response').get('header')

    if response_header.get('resultCode') != '00':
        if response_header.get('resultMsg') == "NO_DATA":
            return json_response.json(), "We got wrong request values :("
    
    else:
        json_response = json_response.get('response').get('body').get('items').get('item')
 
        message = []

        for item in json_response:
            item_pointer = ForecastDataTrimmer()
            item_pointer.category_converter(item)
            
            if item_pointer.weather_value is not None:
                message.append(item_pointer.weather_value)

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

    serviceKey = os.getenv('WEATHER_SECRET_KEY_DECODED')
    target_date = date.today().__format__("%Y%m%d")
    numOfRows = '10'

    request_data = await request.json()

    user_name = request_data.get('action').get('params').get('user_name')

    db_user = crud.get_kakao_user(db, user_name=user_name)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Exists.")

    # user_preferred_time = db_user.user_time # code goes here.
    # user_preferred_time = str(user_preferred_time) # 유저가 원하는 알람 시간이므로 API param에 포함되지 않는다. 나중에 skill관련으로 제공될예정.

    # base time possible setting values = 0200 0500 0800 1100 1400 1700 2000 2300
    # API 제공 시간은 각 base time values += 10분

    # default location set to Seoul
    request_data = {
        'serviceKey' : serviceKey,
        'numOfRows' : numOfRows,
        'pageNo' : '1',
        'dataType' : 'JSON',
        'base_date' : target_date,
        'base_time' : '0200', # base time 중 오늘 날씨까지 제공되는 base time 은 0200 이 유일해보임. (오늘, 내일, 모레 날씨 제공)
        'nx' : db_user.nx,
        'ny' : db_user.ny
    }

    response = get_weather_data(request_data)
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
        "풍속" : response[0],
        "하늘 상태" : response[1],
        "강수 확률" : response[2],
        "현재 강수 상태" : response[3]
    }
    
    return response

@router.put('/edit-user-location', response_model=schemas.KakaoUser)
def edit_user_info(user: schemas.KakaoGetUser, db: Session = Depends(get_db)):
    # the end point router which kakao bot's skill uses.
    # change forecasting location via message.
    db_user = crud.get_kakao_user(db, user_name=user.user_name)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Exists.")
    
    return crud.edit_user_location(db=db, data=user)

@router.put('/edit-user-time', response_model=schemas.KakaoUser)
def edit_user_time(user: schemas.KakaoUserTime, db: Session = Depends(get_db)):
    # the end point router which kakao bot's skill uses.
    # change forecasting time via message.
    db_user = crud.get_kakao_user(db, user_name=user.user_name)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Exists.")

    return crud.edit_user_time(db=db, data=user)

@router.post('/create-kakao-user', response_model=schemas.KakaoUser)
def create_kakao_user(user: schemas.KakaoUser, db: Session = Depends(get_db)):
    db_user = crud.get_kakao_user(db, user_name=user.user_name)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists.")
    
    return crud.create_kakao_user(db=db, data=user)

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