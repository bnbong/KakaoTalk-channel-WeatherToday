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

    def test_could_get_partitional_data_from_api(self):

        self.request_data.update({'numOfRows': '1'})
        response = self.requests.get(self.url, params=self.request_data)

        json_response = self.get_body_items_from_raw_request(response)
        
        assert 1 == len(json_response)

    def test_could_convert_readable_weather_info_with_list(self):
        """
        단기예보 API 코드값 정보
        value of the key 'item' is list.
        
        TMP - 1시간 기온
        TMN - 일 최저 기온
        TMX - 일 최고 기온
        POP - 강수확률
        PTY - 강수형태
        PCP - 1시간 강수량
        REH - 습도
        UUU - 풍속(동서성분)
        VVV - 풍속(남북성분)
        VEC - 풍향
        WSD - 풍속
        SKY - 하늘상태
        WAV - 파고
        SNO - ???
        """
        from ..apps.converter import ForecastDataTrimmer

        self.request_data.update({'numOfRows': '14'})
        response = self.requests.get(self.url, params=self.request_data)

        json_response = self.get_body_items_from_raw_request(response)

        for item in json_response:
            item_pointer = ForecastDataTrimmer()
            item_pointer.category_converter(item)
            print(item_pointer.weather_value)

    def test_could_get_user_id_from_message(self):
        pass


class TestInnerAPI():
    
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_end_point_router(self):
        pass

    def test_add_user_location(self):
        pass

    def test_add_user_time(self):
        pass

    def test_edit_user_location(self):
        pass

    def test_edit_user_time(self):
        pass
