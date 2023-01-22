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
    from dotenv import load_dotenv
    from datetime import date

    import os
    import requests


    load_dotenv()

    @classmethod
    def setup_class(cls):
        
        cls.url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
        cls.serviceKey = cls.os.getenv('WEATHER_SECRET_KEY_DECODED')
        cls.target_date = cls.date.today().__format__("%Y%m%d")
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

        response = cls.requests.get(cls.url, params=cls.request_data)
        cls.response_weather_data_json = response.json().get('response')

    def get_body_items_from_raw_request(self, data):
        response = data.json().get('response').get('body').get('items').get('item')

        return response

    def test_could_get_data_from_weather_api(self):
        
        response = self.response_weather_data_json.get('body').get('items')

        assert '00' == self.response_weather_data_json.get('header').get('resultCode')
        assert None != response
        assert 8 == len(response.get('item')[0].get('baseDate'))

        print(self.response_weather_data_json, self.request_data, response)

    def test_could_get_one_row_data_from_api(self):

        self.request_data.update({'numOfRows': '1'})
        response = self.requests.get(self.url, params=self.request_data)

        json_response = self.get_body_items_from_raw_request(response)
        
        assert 1 == len(json_response)

    def test_could_get_different_time_data_from_api(self):

        self.request_data.update({'base_time': '0200'})
        response = self.requests.get(self.url, params=self.request_data)

        json_response = self.get_body_items_from_raw_request(response)
        
        assert '0200' == (json_response[0].get('baseTime'))

    def test_could_convert_readable_weather_info_with_list(self):
        from ..apps.converter import ForecastDataTrimmer

        self.request_data.update({'numOfRows': '14'})
        response = self.requests.get(self.url, params=self.request_data)

        json_response = self.get_body_items_from_raw_request(response)
 
        message = []

        for item in json_response:
            item_pointer = ForecastDataTrimmer()
            item_pointer.category_converter(item)
            
            if item_pointer.weather_value is not None:
                message.append(item_pointer.weather_value)
        
        assert not None == (message)
        
    def test_could_get_weather_data_from_db_user_info(self):
        from ..apps.user_data_trimmer import UserDataTrimmer
        from ..apps.xlsx_reader import XlsxReader

        from ..api.routing import get_weather_data
        
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

    def test_could_get_user_id_from_message(self):
        # This testcase will be completed after linking Kakao Channel skill.
        pass


class TestInnerAPI():
    from ..db.test_session_maker import client

    @classmethod
    def setup_class(cls):
        from ..db.database import SessionLocal
        from ..db import models

        try:
            db = SessionLocal()
            target_user = db.query(models.KakaoChannelUser).filter(models.KakaoChannelUser.user_name == "NewUser1")
            if target_user:
                db.delete(target_user)
                db.commit()
                db.close()
        except:
            pass
    def test_end_point_router(self):
        pass

    def test_create_kakao_user(self):
        response = self.client.post('/api/v1/create-kakao-user', json={'user_name':'NewUser1', 'user_time':'1200', 'user_location_first':'NewLocation1'})

        assert 200 == (response.status_code)
        assert not None == (response.json())
        assert "NewUser1" == (response.json().get('user_name'))
        assert "1200" == (response.json().get('user_time'))
        assert "NewLocation1" == (response.json().get('user_location_first'))
        assert None == (response.json().get('user_location_second'))

    def test_get_kakao_user_data(self):
        response = self.client.get('/api/v1/get-kakao-user', json={'user_name':'NewUser1'})

        assert 200 == (response.status_code)
        assert not None == (response.json())
        assert "1200" == (response.json().get('user_time'))
        assert "NewLocation1" == (response.json().get('user_location_first'))
        assert None == (response.json().get('user_location_second'))

    def test_edit_user_location(self):
        response = self.client.put('/api/v1/edit-user-location', json={'user_name':'NewUser1','user_location_first':'NewLocation2'})

        assert 200 == (response.status_code)
        assert not None == (response.json())
        assert not "NewLocation1" == (response.json().get('user_location_first'))
        assert "NewLocation2" == (response.json().get('user_location_first'))

    def test_edit_user_time(self):
        response = self.client.put('/api/v1/edit-user-time', json={'user_name':'NewUser1','user_time':'0800'})

        assert 200 == (response.status_code)
        assert not None == (response.json())
        assert not "1200" == (response.json().get('user_time'))
        assert "0800" == (response.json().get('user_time'))
    
    def test_get_kakao_users(self):
        response = self.client.get('/api/v1/get-kakao-users')

        assert 200 == (response.status_code)
        assert "TestUser1" == (response.json()[0].get('user_name'))

    def test_delete_kakao_user(self):
        before_delete = self.client.get('/api/v1/get-kakao-users')

        assert 3 == (len(before_delete.json()))

        response = self.client.delete('/api/v1/delete-kakao-user', json={'user_name':'NewUser1'})

        assert 200 == (response.status_code)
        assert "User successfully deleted." == (response.json())

        after_delete = self.client.get('/api/v1/get-kakao-users')

        assert 2 == (len(after_delete.json()))
