from fastapi import APIRouter, Header
from fastapi.responses import RedirectResponse

from enum import Enum
from typing import Optional, Union

from dotenv import load_dotenv

import os
import requests


load_dotenv()

router = APIRouter()

@router.post('/api/v1/get-daily-forecast')
def get_daily_forecast():
    # the end point router which kakao bot's skill uses.
    pass

@router.post('/api/v1/add-user-location')
def add_user_location():
    # set forecasting location at first.
    pass

@router.post('/api/v1/add-user-time')
def add_user_time():
    # ser forecasting time at first.
    pass

@router.post('/api/v1/edit-user-location')
def edit_user_info():
    # change forecasting location via message.
    pass

@router.post('/api/v1/edit-user-time')
def edit_user_time():
    # change forecasting time via message.
    pass

@router.post('/test')
def test_router():
    pass
