from datetime import datetime, timedelta


class WeatherForecastTrimmer():
    """
        example response:
        {
            'coord': {'lon': 126.9571, 'lat': 37.3939}, 
            'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 날씨 아이콘: https://openweathermap.org/weather-conditions
            'base': 'stations', 
            'main': 
            {
                'temp': -3.78, 기온
                'feels_like': -3.78, 체감 기온
                'temp_min': -4.25, 최저 기온 (전후 3시간)
                'temp_max': -3.15, 최고 기온 (전후 3시간)
                'pressure': 1023, 기압
                'humidity': 60, 습도(퍼센트)
                'sea_level': 1023, 
                'grnd_level': 1018
            }, 
            'visibility': 10000, 가시거리(미터, 최고거리는 10키로)
            'wind': 
            {
                    'speed': 0.63, 풍속
                    'deg': 349, 
                    'gust': 1.72 강풍 풍속
            }, 
            'clouds': {'all': 100}, 구름 양
            'dt': 1674718854, 기상 정보 측정 시간(UTC)
            'sys': {'type': 1, 'id': 5509, 'country': 'KR', 'sunrise': 1674686427, 'sunset': 1674722902}, 일출 일몰 시간(UTC)
            'timezone': 32400, 
            'id': 1846898, 
            'name': 'Anyang-si', 
            'cod': 200
        }
        """
    
    def __init__(self, data):
        self.weather_trimmed_data_json = {}

        self.category_converter(data=data)

    def category_converter(self, data):
        weather_data = data.get('weather')
        main_data = data.get('main')
        visibility_data = data.get('visibility')
        wind_data = data.get('wind')
        clouds_data = data.get('clouds')
        sun_rise_data = data.get('sys').get('sunrise')
        sun_set_data = data.get('sys').get('sunset')

        self.convert_weather(weather_data=weather_data)
        self.convert_main(main_data=main_data)
        self.convert_visibility(visibility_data=visibility_data)
        self.convert_wind(wind_data=wind_data)
        self.convert_cloud(clouds_data=clouds_data)
        self.convert_sun_rise(sun_rise_data=sun_rise_data)
        self.convert_sun_set(sun_set_data=sun_set_data)

    def convert_weather(self, weather_data):
        weather_status = weather_data[0].get('main')
        weather_detail = weather_data[0].get('description')

        self.weather_trimmed_data_json["현재 날씨"] = weather_status
        self.weather_trimmed_data_json["날씨 상세"] = weather_detail

    def convert_main(self, main_data):
        temp_now = main_data.get('temp')
        temp_high = main_data.get('temp_max')
        temp_low = main_data.get('temp_min')
        feeling_temp = main_data.get('feels_like')

        self.weather_trimmed_data_json["현재 온도"] = str(round(temp_now)) + " 도"
        self.weather_trimmed_data_json["체감 온도"] = str(round(feeling_temp)) + " 도"
        self.weather_trimmed_data_json["최고 온도(현재 시각으로부터 전후 3시간)"] = str(round(temp_high)) + " 도"
        self.weather_trimmed_data_json["최저 온도(현재 시각으로부터 전후 3시간)"] = str(round(temp_low)) + " 도"

    def convert_visibility(self, visibility_data):
        #TODO: update km
        self.weather_trimmed_data_json["가시 거리"] = str(visibility_data) + " 미터"

    def convert_wind(self, wind_data):
        wind_speed = wind_data.get('speed')
        
        self.weather_trimmed_data_json["풍속"] = "초속 " + str(wind_speed) + " 미터"

    def convert_cloud(self, clouds_data):
        cloud_amount = clouds_data.get('all')

        self.weather_trimmed_data_json["구름 낀 정도(백분율)"] = str(cloud_amount) + "%"

    def convert_sun_rise(self, sun_rise_data):
        sunrise_time = int(sun_rise_data)

        sunrise_utc_format = datetime.utcfromtimestamp(sunrise_time)
        sunrise_kst = sunrise_utc_format + timedelta(hours=9)
        sunrise_kst_format = sunrise_kst.strftime('%H:%M:%S')

        hour, minute, sec = sunrise_kst_format.split(':')

        self.weather_trimmed_data_json["일출 시간"] = str(hour) + "시 " + str(minute) + "분 " + str(sec) + "초"

    def convert_sun_set(self, sun_set_data):
        sunset_time = int(sun_set_data)

        sunset_utc_format = datetime.utcfromtimestamp(sunset_time)
        sunset_kst = sunset_utc_format + timedelta(hours=9)
        sunset_kst_format = sunset_kst.strftime('%H:%M:%S')

        hour, minute, sec = sunset_kst_format.split(':')

        self.weather_trimmed_data_json["일몰 시간"] = str(hour) + "시 " + str(minute) + "분 " + str(sec) + "초"
