# # TODO: make converter more specific.
#
# class ForecastDataTrimmer():
#     """
#         API가 제공하는 날씨 데이터 정보
#         value of the key 'item' is list.
#
#         TMN - 일 최저 기온
#         TMX - 일 최고 기온
#         POP - 강수확률
#         PTY - 강수형태
#         PCP - 1시간 강수량
#         REH - 습도
#         WSD - 풍속
#         SKY - 하늘상태
#         SNO - 적설양
#     """
#
#     def __init__(self):
#         self.category_list = {"TMP":"1시간 기온", "TMN":"일 최저 기온", "TMX":"일 최고 기온", "POP":"강수확률",
#         "PTY":"강수형태", "PCP":"1시간 강수량", "REH":"습도", "UUU":"풍속(동서성분)", "VVV":"풍속(남북성분)",
#         "VEC":"풍향", "WSD":"풍속", "SKY":"하늘상태", "WAV":"파고", "SNO":"1시간 신적설"}
#         self.category_short = None
#         self.category_long = None
#         self.weather_value = None
#
#     def category_converter(self, data):
#         # this bot will provide SNO, POP, TMX, TMN, PTY, PCP, REH, WSD, SKY information.
#
#         self.category_short = data.get('category')
#         self.category_long = self.category_list.get(self.category_short)
#         self.calculate_weather_value(self.category_short, data.get('fcstValue'))
#
#     def calculate_weather_value(self, category, fcstValue):
#         match category:
#             case "PCP" :
#                 self.pcp_calculator(fcstValue)
#             case "SNO":
#                 self.sno_calculator(fcstValue)
#             case "POP":
#                 self.pop_calculator(fcstValue)
#             case "SKY":
#                 self.sky_calculator(fcstValue)
#             case "WSD":
#                 self.wsd_calculator(fcstValue)
#             case "TMN":
#                 self.tmn_calculator(fcstValue)
#             case "TMX":
#                 self.tmx_calculator(fcstValue)
#             case "PTY":
#                 self.pty_calculator(fcstValue)
#             case "REH":
#                 self.reh_calculator(fcstValue)
#
#     def pcp_calculator(self, value):
#         if value == "강수없음":
#             self.weather_value = value
#         else:
#             value = value[:-2]
#             if float(value) < (float)(1.0):
#                 self.weather_value = "1.0mm 미만"
#             elif float(value) < (float)(30.0):
#                 self.weather_value = "1.0 ~ 29.0mm"
#             elif float(value) < (float)(50.0):
#                 self.weather_value = "30.0 ~ 50.0mm"
#             else:
#                 self.weather_value = "50.0mm 이상"
#
#     def sno_calculator(self, value):
#         if value == "적설없음":
#             self.weather_value = value
#         elif float(value) < (float)(1.0):
#             self.weather_value = "1.0cm 미만"
#         elif float(value) < (float)(5.0):
#             self.weather_value = value + "cm"
#         else:
#             self.weather_value = "5.0cm 이상"
#
#     def pop_calculator(self, value):
#         self.weather_value = "강수확률 : " + value + "%"
#
#     def tmn_calculator(self, value):
#         self.weather_value = "최저기온" + value + "C"
#
#     def tmx_calculator(self, value):
#         self.weather_value = "최고기온" + value + "C"
#
#     def pty_calculator(self, value):
#         match value:
#             case 0:
#                 self.weather_value = "강수 없음"
#             case 1:
#                 self.weather_value = "비"
#             case 2:
#                 self.weather_value = "비 또는 눈"
#             case 3:
#                 self.weather_value = "눈"
#             case 4:
#                 self.weather_value = "소나기"
#
#     def reh_calculator(self, value):
#         self.weather_value = "습도 : " + value + "%"
#
#     def wsd_calculator(self, value):
#         if float(value) < 4:
#             self.weather_value = "약한 바람"
#         elif float(value) < 9:
#             self.weather_value = "약간 강한 바람"
#         elif float(value) < 14:
#             self.weather_value = "강한 바람"
#         else:
#             self.weather_value = "매우 강한 바람"
#
#     def sky_calculator(self, value):
#         if int(value) < 6:
#             self.weather_value = "맑음"
#         elif int(value) < 9:
#             self.weather_value = "구름많음"
#         else:
#             self.weather_value = "흐림"
#


# class WeatherForecastTrimmer:
#     """example response:
#     {
#         'coord': {'lon': 126.9571, 'lat': 37.3939},
#         'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 날씨 아이콘: https://openweathermap.org/weather-conditions
#         'base': 'stations',
#         'main':
#         {
#             'temp': -3.78, 기온
#             'feels_like': -3.78, 체감 기온
#             'temp_min': -4.25, 최저 기온 (전후 3시간)
#             'temp_max': -3.15, 최고 기온 (전후 3시간)
#             'pressure': 1023, 기압
#             'humidity': 60, 습도(퍼센트)
#             'sea_level': 1023,
#             'grnd_level': 1018
#         },
#         'visibility': 10000, 가시거리(미터, 최고거리는 10키로)
#         'wind':
#         {
#                 'speed': 0.63, 풍속
#                 'deg': 349,
#                 'gust': 1.72 강풍 풍속
#         },
#         'clouds': {'all': 100}, 구름 양
#         'dt': 1674718854, 기상 정보 측정 시간(UTC)
#         'sys': {'type': 1, 'id': 5509, 'country': 'KR', 'sunrise': 1674686427, 'sunset': 1674722902}, 일출 일몰 시간(UTC)
#         'timezone': 32400,
#         'id': 1846898,
#         'name': 'Anyang-si',
#         'cod': 200
#     }
#     """
#
#     def __init__(self, data):
#         self.weather_trimmed_data_json = {}
#
#         self.category_converter(data=data)
#
#     def category_converter(self, data):
#         # self.weather_trimmed_data_json["도시 이름"] = data.get('name')
#
#         weather_data = data.get("weather")
#         main_data = data.get("main")
#         visibility_data = data.get("visibility")
#         wind_data = data.get("wind")
#         clouds_data = data.get("clouds")
#         sun_rise_data = data.get("sys").get("sunrise")
#         sun_set_data = data.get("sys").get("sunset")
#
#         self.convert_weather(weather_data=weather_data)
#         self.convert_main(main_data=main_data)
#         self.convert_visibility(visibility_data=visibility_data)
#         self.convert_wind(wind_data=wind_data)
#         self.convert_cloud(clouds_data=clouds_data)
#         self.convert_sun_rise(sun_rise_data=sun_rise_data)
#         self.convert_sun_set(sun_set_data=sun_set_data)
#
#     def convert_weather(self, weather_data):
#         weather_status = weather_data[0].get("main")
#         weather_detail = weather_data[0].get("description")
#
#         self.weather_trimmed_data_json["weather_info"] = weather_status
#         self.weather_trimmed_data_json["weather_detail"] = weather_detail
#
#     def convert_main(self, main_data):
#         temp_now = main_data.get("temp")
#         temp_high = main_data.get("temp_max")
#         temp_low = main_data.get("temp_min")
#         feeling_temp = main_data.get("feels_like")
#
#         self.weather_trimmed_data_json["temperature"] = str(round(temp_now)) + " 도"
#         self.weather_trimmed_data_json["feeling_temperature"] = (
#             str(round(feeling_temp)) + " 도"
#         )
#         self.weather_trimmed_data_json["high_temperature"] = (
#             str(round(temp_high)) + " 도"
#         )
#         self.weather_trimmed_data_json["low_temperature"] = str(round(temp_low)) + " 도"
#
#     def convert_visibility(self, visibility_data):
#         # TODO: update km
#         self.weather_trimmed_data_json["visibility"] = str(visibility_data) + " 미터"
#
#     def convert_wind(self, wind_data):
#         wind_speed = wind_data.get("speed")
#
#         self.weather_trimmed_data_json["wind_speed"] = "초속 " + str(wind_speed) + " 미터"
#
#     def convert_cloud(self, clouds_data):
#         cloud_amount = clouds_data.get("all")
#
#         self.weather_trimmed_data_json["cloud_percentage"] = str(cloud_amount) + "%"
#
#     def convert_sun_rise(self, sun_rise_data):
#         sunrise_time = int(sun_rise_data)
#
#         sunrise_utc_format = datetime.utcfromtimestamp(sunrise_time)
#         sunrise_kst = sunrise_utc_format + timedelta(hours=9)
#         sunrise_kst_format = sunrise_kst.strftime("%H:%M:%S")
#
#         hour, minute, sec = sunrise_kst_format.split(":")
#
#         self.weather_trimmed_data_json["sunrise_time"] = (
#             str(hour) + "시 " + str(minute) + "분 " + str(sec) + "초"
#         )
#
#     def convert_sun_set(self, sun_set_data):
#         sunset_time = int(sun_set_data)
#
#         sunset_utc_format = datetime.utcfromtimestamp(sunset_time)
#         sunset_kst = sunset_utc_format + timedelta(hours=9)
#         sunset_kst_format = sunset_kst.strftime("%H:%M:%S")
#
#         hour, minute, sec = sunset_kst_format.split(":")
#
#         self.weather_trimmed_data_json["sunset_time"] = (
#             str(hour) + "시 " + str(minute) + "분 " + str(sec) + "초"
#         )
