# TODO: make Kakao Bot channel skills and link it.
from fastapi import APIRouter, Header
from fastapi.responses import RedirectResponse

from enum import Enum
from typing import Optional, Union
from datetime import date

from dotenv import load_dotenv

from ..apps.xlsx_reader import XlsxReader
from ..apps.converter import ForecastDataTrimmer

import os
import requests


load_dotenv()

router = APIRouter()

def get_weather_data(request_data):
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    
    response = requests.get(url, params=request_data)
    response_weather_data_json = response.json().get('response')

    return response_weather_data_json

def get_body_items_from_raw_request(data):
    response = data.get('body').get('items').get('item')

    return response

@router.post('/get-daily-forecast')
def get_daily_forecast():
    # the end point router which kakao bot's skill uses.
    serviceKey = os.getenv('WEATHER_SECRET_KEY_DECODED')
    target_date = date.today().__format__("%Y%m%d")
    numOfRows = '14'

    user_detailed_location_json = {} # code goes here.
    nx, ny = XlsxReader().filter_xlsx_data(user_detailed_location_json)

    user_preferred_time = '0500' # code goes here.

    # default location set to Gangnam
    request_data = {
        'serviceKey' : serviceKey,
        'numOfRows' : numOfRows,
        'pageNo' : '1',
        'dataType' : 'JSON',
        'base_date' : target_date,
        'base_time' : user_preferred_time, # change user's info - user_time col
        'nx' : nx, # change user's info - using with user_location_first, etc.. col
        'ny' : ny # change user's info - using with user_location_first, etc.. col
    }

    response = get_weather_data(request_data)
    json_response = get_body_items_from_raw_request(response)
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
    message = []

    for item in json_response:
        item_pointer = ForecastDataTrimmer()
        item_pointer.category_converter(item)

        if item_pointer.weather_value is not None:
            message.append(item_pointer.weather_value)

    return message

@router.post('/edit-user-location')
def edit_user_info():
    # the end point router which kakao bot's skill uses.
    # change forecasting location via message.
    pass

@router.post('/edit-user-time')
def edit_user_time():
    # the end point router which kakao bot's skill uses.
    # change forecasting time via message.
    pass
