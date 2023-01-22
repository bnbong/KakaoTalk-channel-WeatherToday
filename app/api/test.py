from dotenv import load_dotenv
from datetime import date

from .routing import get_weather_data, get_ultimate_weather_data

import os
import pytest


load_dotenv()


class TestUtil():

    def test_split_datetime(self):
        from datetime import date

        formatted_date_string = date.today().__format__("%Y%m%d")
        
        assert 8 == (len(formatted_date_string))

    def test_changing_json_string(self):
        request_data = {
            'serviceKey' : 'this_is_service_key',
            'numOfRows' : '10',
            'pageNo' : '1',
            'dataType' : 'JSON',
            'base_date' : '20000210',
            'base_time' : '0500',
            'nx' : '100',
            'ny' : '200'
        }

        assert '10' == (request_data.get('numOfRows'))

        request_data.update({'numOfRows':'1'})

        assert 8 == (len(request_data))
        assert '1' == (request_data.get('numOfRows'))


class TestOuterAPI():
    import requests


    @classmethod
    def setup_class(cls):
        cls.url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
        cls.serviceKey = os.getenv('WEATHER_SECRET_KEY_DECODED')
        cls.target_date = date.today().__format__("%Y%m%d")
        cls.numOfRows = '10'
        nx = '61'
        ny = '126'

        # location set to Gangnam
        cls.request_data = {
            'serviceKey' : cls.serviceKey,
            'numOfRows' : cls.numOfRows,
            'pageNo' : '1',
            'dataType' : 'JSON',
            'base_date' : cls.target_date,
            'base_time' : '0500',
            'nx' : nx,
            'ny' : ny
        }

        cls.kakao_request = {
            "intent": {
                "id": "6n254h25rfd7cgw31hlgwber",
                "name": "블록 이름"
            },
            "userRequest": {
                "timezone": "Asia/Seoul",
                "params": {
                "ignoreMe": "true"
                },
                "block": {
                "id": "6n254h25rfd7cgw31hlgwber",
                "name": "블록 이름"
                },
                "utterance": "발화 내용",
                "lang": None,
                "user": {
                "id": "866540",
                "type": "accountId",
                "properties": {}
                }
            },
            "bot": {
                "id": "62fb6c0370055f434dcd360f",
                "name": "봇 이름"
            },
            "action": {
                "name": "olutzmbfur",
                "clientExtra": None,
                "params": {
                "user_name": "TestUser0"
                },
                "id": "gwnjegxd1ujww6j3hccpjtnc",
                "detailParams": {
                    "user_name": {
                        "origin": "TestUser0",
                        "value": "TestUser0",
                        "groupName": ""
                    }
                }
            }
        }

        response = cls.requests.get(cls.url, params=cls.request_data)
        cls.response_weather_data_json = response.json().get('response')

    @pytest.mark.skip(reason="too many return")
    def test_could_get_data_from_weather_api(self):
        response = self.response_weather_data_json.get('body').get('items')

        assert '00' == self.response_weather_data_json.get('header').get('resultCode')
        assert None != response
        assert 8 == len(response.get('item')[0].get('baseDate'))

        print(self.response_weather_data_json, self.request_data, response)

    def test_could_get_one_row_data_from_api(self):
        self.request_data.update({'numOfRows': '1'})
        response = self.requests.get(self.url, params=self.request_data)

        json_response = response.json()
        
        assert 1 == len(json_response)

    def test_could_get_different_time_data_from_api(self):
        self.request_data.update({'base_time': '0200'})
        response = self.requests.get(self.url, params=self.request_data)

        json_response = response.json().get('response').get('body').get('items').get('item')
        
        assert '0200' == (json_response[0].get('baseTime'))

    def test_could_convert_readable_weather_info_with_list(self):
        from ..apps.converter import ForecastDataTrimmer

        self.request_data.update({'numOfRows': '14'})
        response = self.requests.get(self.url, params=self.request_data)

        json_response = response.json().get('response').get('body').get('items').get('item')
 
        message = []

        for item in json_response:
            item_pointer = ForecastDataTrimmer()
            item_pointer.category_converter(item)
            
            if item_pointer.weather_value is not None:
                message.append(item_pointer.weather_value)
        
        assert not None == (message)
    
    @pytest.mark.skip(reason="too long return time")
    def test_could_get_weather_data_from_db_user_info(self):
        from ..apps.user_data_trimmer import UserDataTrimmer
        from ..apps.xlsx_reader import XlsxReader


        test_location_json = UserDataTrimmer().convert_user_locations_into_readable_data("경기도", "성남시분당구",None)
        nx, ny = XlsxReader().filter_xlsx_data(test_location_json)
        nx, ny = str(nx), str(ny)

        request_data = {
            'serviceKey' : self.serviceKey,
            'numOfRows' : self.numOfRows,
            'pageNo' : '1',
            'dataType' : 'JSON',
            'base_date' : self.target_date,
            'base_time' : '0200', # change user's info - user_time col
            'nx' : nx, # change user's info - using with user_location_first, etc.. col
            'ny' : ny # change user's info - using with user_location_first, etc.. col
        }

        response = get_weather_data(request_data)

        print(response)


class TestInnerAPI():
    from ..test_session_maker import client
    from ..db import crud


    @classmethod
    def setup_class(cls):
        cls.url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
        cls.serviceKey = os.getenv('WEATHER_SECRET_KEY_DECODED')
        cls.target_date = date.today().__format__("%Y%m%d")
        cls.numOfRows = '10'

        try:
            if cls.client.get('/api/v1/get-kakao-user', json={'user_name':'NewUser1'}):
                cls.client.delete('/api/v1/delete-kakao-user', json={'user_name':'NewUser1'})
            cls.client.post('/api/v1/create-kakao-user', json={'user_name':'TestUser0', 'user_time':'1000','user_location_first':'TestLocation0'})
            cls.client.post('/api/v1/create-kakao-user', json={'user_name':'TestUser1'})
        except:
            pass

    @classmethod
    def teardown_class(cls):
        try:
            cls.client.delete('/api/v1/delete-kakao-user', json={'user_name':'TestUser0'})
            cls.client.delete('/api/v1/delete-kakao-user', json={'user_name':'TestUser1'})
        except:
            pass

    def test_end_pointer_router(self):
        from ..test_session_maker import TestingSessionLocal

        import requests


        request = {
            "intent": {
                "id": "6n254h25rfd7cgw31hlgwber",
                "name": "블록 이름"
            },
            "userRequest": {
                "timezone": "Asia/Seoul",
                "params": {
                "ignoreMe": "true"
                },
                "block": {
                "id": "6n254h25rfd7cgw31hlgwber",
                "name": "블록 이름"
                },
                "utterance": "발화 내용",
                "lang": None,
                "user": {
                "id": "866540",
                "type": "accountId",
                "properties": {}
                }
            },
            "bot": {
                "id": "62fb6c0370055f434dcd360f",
                "name": "봇 이름"
            },
            "action": {
                "name": "olutzmbfur",
                "clientExtra": None,
                "params": {
                "user_name": "TestUser0"
                },
                "id": "gwnjegxd1ujww6j3hccpjtnc",
                "detailParams": {
                    "user_name": {
                        "origin": "TestUser0",
                        "value": "TestUser0",
                        "groupName": ""
                    }
                }
            }
        }

        user_name = request.get('action').get('params').get('user_name')

        db_user = self.crud.get_kakao_user(TestingSessionLocal(), user_name=user_name)

        nx = str(db_user.nx)
        ny = str(db_user.ny)

        request_data = {
            'serviceKey' : self.serviceKey,
            'numOfRows' : self.numOfRows,
            'pageNo' : '1',
            'dataType' : 'JSON',
            'base_date' : self.target_date,
            'base_time' : '0200', # change user's info - user_time col
            'nx' : nx, # change user's info - using with user_location_first, etc.. col
            'ny' : ny # change user's info - using with user_location_first, etc.. col
        }

        response = get_weather_data(request_data)

        assert list == type(response)
        assert not None == response

    def test_create_kakao_user(self):
        response = self.client.post('/api/v1/create-kakao-user', json={'user_name':'NewUser1', 'user_location_first':'NewLocation1'})

        assert 200 == (response.status_code)
        assert not None == (response.json())
        assert "NewUser1" == (response.json().get('user_name'))
        assert "0800" == (response.json().get('user_time'))
        assert "NewLocation1" == (response.json().get('user_location_first'))
        assert None == (response.json().get('user_location_second'))

    def test_get_new_kakao_user_data(self):
        response = self.client.get('/api/v1/get-kakao-user', json={'user_name':'NewUser1'})

        assert 200 == (response.status_code)
        assert not None == (response.json())
        assert "0800" == (response.json().get('user_time'))
        assert "NewLocation1" == (response.json().get('user_location_first'))
        assert None == (response.json().get('user_location_second'))
    
    def test_get_existing_kakao_user_data_0(self):
        response = self.client.get('/api/v1/get-kakao-user', json={'user_name':'TestUser0'})

        assert 200 == (response.status_code)
        assert not None == (response.json())
        assert "1000" == (response.json().get('user_time'))
        assert "TestLocation0" == (response.json().get('user_location_first'))
        assert None == (response.json().get('user_location_second'))
        assert True == (response.json().get('is_active'))

    def test_get_existing_kakao_user_data_1(self):
        response = self.client.get('/api/v1/get-kakao-user', json={'user_name':'TestUser1'})

        assert 200 == (response.status_code)
        assert not None == (response.json())
        assert "0800" == (response.json().get('user_time'))
        assert None == (response.json().get('user_location_first'))
        assert None == (response.json().get('user_location_second'))
        assert True == (response.json().get('is_active'))

    def test_edit_user_location(self):
        response = self.client.put('/api/v1/edit-user-location', json={'user_name':'NewUser1','user_location_first':'NewLocation2'})

        assert 200 == (response.status_code)
        assert not None == (response.json())
        assert not "NewLocation1" == (response.json().get('user_location_first'))
        assert "NewLocation2" == (response.json().get('user_location_first'))

    def test_edit_user_time(self):
        response = self.client.put('/api/v1/edit-user-time', json={'user_name':'NewUser1','user_time':'1200'})

        assert 200 == (response.status_code)
        assert not None == (response.json())
        assert not "0800" == (response.json().get('user_time'))
        assert "1200" == (response.json().get('user_time'))
    
    def test_get_kakao_users(self):
        response = self.client.get('/api/v1/get-kakao-users')

        assert 200 == (response.status_code)
        assert not None == (response.json())

    # @pytest.mark.skip(reason="")
    def test_delete_kakao_user(self):
        before_delete = self.client.get('/api/v1/get-kakao-users')

        assert 3 == (len(before_delete.json()))

        response = self.client.delete('/api/v1/delete-kakao-user', json={'user_name':'NewUser1'})

        assert 200 == (response.status_code)
        assert "User successfully deleted." == (response.json())

        after_delete = self.client.get('/api/v1/get-kakao-users')

        assert 2 == (len(after_delete.json()))
