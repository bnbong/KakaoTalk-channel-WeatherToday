# TODO: make Kakao Bot channel skills and link it.
from fastapi import APIRouter, HTTPException, Depends

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
    response_weather_data = response.json().get('response')

    if response_weather_data.get('header').get('resultCode') != '00':
        if response_weather_data.get('header').get('resultMsg') == "NO_DATA":
            msg = request_data
            return msg, response.json(), "We got wrong request values :("
    
    else:
        response_json = response_weather_data.get('body').get('items').get('item')
        message = []

        for item in response_json:
            item_pointer = ForecastDataTrimmer()
            item_pointer.category_converter(item)

            if item_pointer.weather_value is not None:
                message.append(item_pointer.weather_value)

        return message

@router.get('/')
def get_test_response():
    response = 'this is test api'

    return response

@router.post('/get-daily-forecast')
def get_daily_forecast(user: schemas.KakaoGetUser, db: Session = Depends(get_db)):
    # the end point router which kakao bot's skill uses.
    serviceKey = os.getenv('WEATHER_SECRET_KEY_DECODED')
    target_date = date.today().__format__("%Y%m%d")
    numOfRows = '10'

    db_user = crud.get_kakao_user(db, user_name=user.user_name)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Exists.")
    
    user_detailed_location_json = UserDataTrimmer().convert_user_locations_into_readable_data(db_user.user_location_first, db_user.user_location_second, db_user.user_location_third) # code goes here.
    try:
        nx, ny = XlsxReader().filter_xlsx_data(user_detailed_location_json)
        nx, ny = str(nx), str(ny)
    except IndexError as e:
        # if location cannot found at xlsx db, default location will be set at Seoul.
        nx, ny = '61', '126'

    user_preferred_time = db_user.user_time # code goes here.
    user_preferred_time = str(user_preferred_time) # 유저가 원하는 알람 시간이므로 API param에 포함되지 않는다. 나중에 skill관련으로 제공될예정.

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
        'nx' : nx,
        'ny' : ny
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
def edit_user_time(user: schemas.KakaoUserCreate, db: Session = Depends(get_db)):
    # the end point router which kakao bot's skill uses.
    # change forecasting time via message.
    db_user = crud.get_kakao_user(db, user_name=user.user_name)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Exists.")

    return crud.edit_user_time(db=db, data=user)

@router.post('/create-kakao-user', response_model=schemas.KakaoUser)
def create_kakao_user(user: schemas.KakaoUserCreate, db: Session = Depends(get_db)):
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