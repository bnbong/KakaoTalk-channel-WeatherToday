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
        serviceKey = cls.os.getenv('WEATHER_SECRET_KEY_DECODED')
        target_date = cls.date.today().__format__("%Y%m%d")
        numOfRows = '10'
        nx = '61'
        ny = '126'

        # location set to Gangnam
        cls.request_data = {
            'serviceKey' : serviceKey,
            'numOfRows' : numOfRows,
            'pageNo' : '1',
            'dataType' : 'JSON',
            'base_date' : target_date,
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

        print(response)

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

    def test_could_get_user_id_from_message(self):
        pass


class TestInnerAPI():
    from ..apps.test_session_maker import client

    @classmethod
    def setup_class(cls):    
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_end_point_router(self):
        response = self.client.post('/api/v1/get-daily-forecast')

        assert 200 == (response.status_code)
        assert not None == (response.json())

    def test_edit_user_location(self):
        response = self.client.post('/api/v1/edit-user-location')

        assert 200 == (response.status_code)
        # assert not None == (response.json())

    def test_edit_user_time(self):
        response = self.client.post('/api/v1/edit-user-time')

        assert 200 == (response.status_code)
        # assert not None == (response.json())
