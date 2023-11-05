import pytest_asyncio

from app.src.utils.xlsx_reader import XlsxReader


class TestUtils:
    @classmethod
    def setup_class(cls):
        cls.xlsx_pointer = XlsxReader()

    async def test_could_read_xlsx_data(self):
        result = self.xlsx_pointer.get_all_xlsx_data()

        assert 60 == (result[0])
        assert 127 == (result[1])

    async def test_could_get_nx_ny_from_formatted_user_location_data(self):
        location_name = "백현동"
        result = self.xlsx_pointer.filter_xlsx_data(location_name)

        assert (62, 123) == (result[0], result[1])

        location_name = "경기도"
        result = self.xlsx_pointer.filter_xlsx_data(location_name)

        assert (60, 120) == (result[0], result[1])

        location_name = "성남시"
        result = self.xlsx_pointer.filter_xlsx_data(location_name)

        assert (63, 124) == (result[0], result[1])


# import pytest
#
#
# class TestNewWeatherAPI:
#     def test_UTC_converter(self):
#         from datetime import datetime, timedelta
#
#         sunrise_time = "1674686390"
#         sunset_time = "1674722858"
#
#         sunrise_time = int(sunrise_time)
#         sunset_time = int(sunset_time)
#
#         sunrise_utc_format = datetime.utcfromtimestamp(sunrise_time)
#         sunrise_kst = sunrise_utc_format + timedelta(hours=9)
#         sunrise_kst_format = sunrise_kst.strftime("%H:%M:%S")
#
#         hour, minute, sec = sunrise_kst_format.split(":")
#
#         assert ("07", "39", "50") == (hour, minute, sec)
#
#         sunset_utc_format = datetime.utcfromtimestamp(sunset_time)
#         sunset_kst = sunset_utc_format + timedelta(hours=9)
#         sunset_kst_format = sunset_kst.strftime("%H:%M:%S")
#
#         hour, minute, sec = sunset_kst_format.split(":")
#
#         assert ("17", "47", "38") == (hour, minute, sec)
#
#
# @pytest.mark.skip(reason="testing another api")
# class TestWeatherInfo:
#     @classmethod
#     def setup_class(cls):
#         from .weather_info import WeatherInfo
#
#         cls.weather_info = WeatherInfo()
#
#     def test_weather_is_too_cold(self):
#         # informs to get thick clothes.
#         pass
#
#     def test_weather_is_too_hot(self):
#         # informs to get thin clothes.
#         pass
#
#     def test_weather_is_good(self):
#         # informs it's good to go picnic.
#         pass
#
#     def test_will_be_rain_today(self):
#         # informs pty, and to get umbrella and raincoat.
#         pass
#
#     def test_will_be_snow_today(self):
#         # informs sno, and be care of frozen road when driving.
#         pass
#
#     def test_will_be_tstm_today(self):
#         # informs to be careful not to be fly.
#         pass
#
#     def test_temperature_drops_hard(self):
#         # informs temperature drops hard, so be careful at clothes.
#         pass
#
#     def test_temperature_rises_hard(self):
#         # informs temperature rises hard, so be careful at clothes.
#         pass
