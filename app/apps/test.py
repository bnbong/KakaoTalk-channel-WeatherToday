import pytest


class TestNewWeatherAPI():

    def test_UTC_converter(self):
        from datetime import datetime, timedelta

        sunrise_time = '1674686390'
        sunset_time = '1674722858'

        sunrise_time = int(sunrise_time)
        sunset_time = int(sunset_time)

        sunrise_utc_format = datetime.utcfromtimestamp(sunrise_time)
        sunrise_kst = sunrise_utc_format + timedelta(hours=9)
        sunrise_kst_format = sunrise_kst.strftime('%H:%M:%S')

        hour, minute, sec = sunrise_kst_format.split(':')

        assert ("07", "39", "50") == (hour, minute, sec)
        
        sunset_utc_format = datetime.utcfromtimestamp(sunset_time)
        sunset_kst = sunset_utc_format + timedelta(hours=9)
        sunset_kst_format = sunset_kst.strftime('%H:%M:%S')

        hour, minute, sec = sunset_kst_format.split(':')

        assert ("17", "47", "38") == (hour, minute, sec)


@pytest.mark.skip(reason="testing another api")
class TestWeatherInfo():
    
    @classmethod
    def setup_class(cls):
        from .weather_info import WeatherInfo

        cls.weather_info = WeatherInfo()

    def test_weather_is_too_cold(self):
        # informs to get thick clothes.
        pass

    def test_weather_is_too_hot(self):
        # informs to get thin clothes.
        pass

    def test_weather_is_good(self):
        # informs it's good to go picnic.
        pass

    def test_will_be_rain_today(self):
        # informs pty, and to get umbrella and raincoat.
        pass

    def test_will_be_snow_today(self):
        # informs sno, and be care of frozen road when driving.
        pass

    def test_will_be_tstm_today(self):
        # informs to be careful not to be fly.
        pass

    def test_temperature_drops_hard(self):
        # informs temperature drops hard, so be careful at clothes.
        pass

    def test_temperature_rises_hard(self):
        # informs temperature rises hard, so be careful at clothes.
        pass


class TestMessageConverter():
    
    def test_could_convert_readable_weather_info_with_list(self):
        # from ..apps.converter import ForecastDataTrimmer

        # self.request_data.update({'numOfRows': '14'})
        # response = self.requests.get(self.url, params=self.request_data)

        # json_response = response.json().get('response').get('body').get('items').get('item')
 
        # message = []

        # for item in json_response:
        #     item_pointer = ForecastDataTrimmer()
        #     item_pointer.category_converter(item)
            
        #     if item_pointer.weather_value is not None:
        #         message.append(item_pointer.weather_value)
        
        # assert not None == (message)
        pass
