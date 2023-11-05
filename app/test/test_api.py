import pytest_asyncio

from httpx import AsyncClient


class TestAPI:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, app_client: AsyncClient):
        pass

    async def test_ping(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.get("/kakao-weather-bot/api/v1/_ping")

        # then
        assert response.status_code == 200
        assert response.json() == {"message": "pong!"}

    async def test_create_user(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.post(
            "/kakao-weather-bot/api/v1/user/",
            json={
                "user_name": "Test User",
                "is_active": True,
            },
        )

        # then
        data = response.json()
        assert response.status_code == 200
        assert data["user_name"] == "Test User"
        assert data["is_active"] == True
        assert data["user_time"] == "0800"
        assert data["user_location"] == "서울특별시"

    async def test_get_weather_data(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.post(
            "/kakao-weather-bot/api/v1/daily-forecast",
            json={
                "user_name": "Test User",
            },
        )

        # then
        print(response.json())
        data = response.json()
        assert response.status_code == 200
        assert data is not None
        assert data["풍속"] is not None

    async def test_get_user_data(self, app_client: AsyncClient):
        pass

    async def test_edit_user_data(self, app_client: AsyncClient):
        pass

    async def test_delete_user_data(self, app_client: AsyncClient):
        pass


# class TestOuterAPI:
#     import requests
#
#     @classmethod
#     def setup_class(cls):
#         cls.api_key = os.getenv("WEATHER_API_KEY")
#         cls.city_name = "서울특별시"
#         cls.url = f"https://api.openweathermap.org/data/2.5/weather?q={cls.city_name}&appid={cls.api_key}&units=metric&lang=kr"
#
#         cls.request_data = {"api_key": cls.api_key, "city_name": cls.city_name}
#
#         cls.kakao_request = {
#             "intent": {"id": "6n254h25rfd7cgw31hlgwber", "name": "블록 이름"},
#             "userRequest": {
#                 "timezone": "Asia/Seoul",
#                 "params": {"ignoreMe": "true"},
#                 "block": {"id": "6n254h25rfd7cgw31hlgwber", "name": "블록 이름"},
#                 "utterance": "발화 내용",
#                 "lang": None,
#                 "user": {"id": "866540", "type": "accountId", "properties": {}},
#             },
#             "bot": {"id": "62fb6c0370055f434dcd360f", "name": "봇 이름"},
#             "action": {
#                 "name": "olutzmbfur",
#                 "clientExtra": None,
#                 "params": {"user_name": "TestUser0"},
#                 "id": "gwnjegxd1ujww6j3hccpjtnc",
#                 "detailParams": {
#                     "user_name": {
#                         "origin": "TestUser0",
#                         "value": "TestUser0",
#                         "groupName": "",
#                     }
#                 },
#             },
#         }
#
#         response = cls.requests.get(cls.url, params=cls.request_data)
#         cls.response_weather_data_json = response.json()
#
#     def test_could_get_data_from_weather_api(self):
#         assert 200 == (self.response_weather_data_json.get("cod"))
#
#         print(self.response_weather_data_json)
#
#     def test_could_get_weather_data_from_db_user_info(self):
#         # from ..apps.user_data_trimmer import UserDataTrimmer
#         # from ..apps.xlsx_reader import XlsxReader
#
#         # test_location_json = UserDataTrimmer().convert_user_locations_into_readable_data("경기도", "성남시분당구",None)
#         # nx, ny = XlsxReader().filter_xlsx_data(test_location_json)
#         # nx, ny = str(nx), str(ny)
#
#         # request_data = {
#         #     'serviceKey' : self.serviceKey,
#         #     'numOfRows' : self.numOfRows,
#         #     'pageNo' : '1',
#         #     'dataType' : 'JSON',
#         #     'base_date' : self.target_date,
#         #     'base_time' : '0200', # change user's info - user_time col
#         #     'nx' : nx, # change user's info - using with user_location_first, etc.. col
#         #     'ny' : ny # change user's info - using with user_location_first, etc.. col
#         # }
#
#         # response = get_weather_data(request_data)
#
#         # print(response)
#         pass
#
#
# class TestInnerAPI:
#     from test.conftest import client
#     from ..db import crud
#
#     @classmethod
#     def setup_class(cls):
#         cls.api_key = os.getenv("WEATHER_API_KEY")
#         cls.city_name = "성남시"
#         cls.url = f"https://api.openweathermap.org/data/2.5/weather?q={cls.city_name}&appid={cls.api_key}&units=metric&lang=kr"
#
#         try:
#             if cls.client.get("/api/v1/get-kakao-user", json={"user_name": "NewUser1"}):
#                 cls.client.delete(
#                     "/api/v1/delete-kakao-user", json={"user_name": "NewUser1"}
#                 )
#             cls.client.post(
#                 "/api/v1/create-kakao-user",
#                 json={
#                     "user_name": "TestUser0",
#                     "user_time": "1000",
#                     "user_location": "TestLocation0",
#                 },
#             )
#             cls.client.post(
#                 "/api/v1/create-kakao-user", json={"user_name": "TestUser1"}
#             )
#         except:
#             pass
#
#     @classmethod
#     def teardown_class(cls):
#         try:
#             cls.client.delete(
#                 "/api/v1/delete-kakao-user", json={"user_name": "TestUser0"}
#             )
#             cls.client.delete(
#                 "/api/v1/delete-kakao-user", json={"user_name": "TestUser1"}
#             )
#         except:
#             pass
#
#     def test_end_pointer_router(self):
#         from test.conftest import TestingSessionLocal
#
#         request = {
#             "intent": {"id": "6n254h25rfd7cgw31hlgwber", "name": "블록 이름"},
#             "userRequest": {
#                 "timezone": "Asia/Seoul",
#                 "params": {"ignoreMe": "true"},
#                 "block": {"id": "6n254h25rfd7cgw31hlgwber", "name": "블록 이름"},
#                 "utterance": "발화 내용",
#                 "lang": None,
#                 "user": {"id": "866540", "type": "accountId", "properties": {}},
#             },
#             "bot": {"id": "62fb6c0370055f434dcd360f", "name": "봇 이름"},
#             "action": {
#                 "name": "olutzmbfur",
#                 "clientExtra": None,
#                 "params": {"user_name": "TestUser0"},
#                 "id": "gwnjegxd1ujww6j3hccpjtnc",
#                 "detailParams": {
#                     "user_name": {
#                         "origin": "TestUser0",
#                         "value": "TestUser0",
#                         "groupName": "",
#                     }
#                 },
#             },
#         }
#
#         user_name = request.get("action").get("params").get("user_name")
#
#         db_user = self.crud.get_kakao_user(TestingSessionLocal(), user_name=user_name)
#
#         request_data = {"api_key": self.api_key, "city_name": self.city_name}
#
#         response = get_weather_data(request_data)
#
#         assert dict == type(response)
#         assert not None == response
#
#         print(response)
#
#     def test_create_kakao_user(self):
#         response = self.client.post(
#             "/api/v1/create-kakao-user",
#             json={"user_name": "NewUser1", "user_location": "NewLocation1"},
#         )
#
#         assert 200 == (response.status_code)
#         assert not None == (response.json())
#         assert "NewUser1" == (response.json().get("user_name"))
#         assert "0800" == (response.json().get("user_time"))
#         assert "NewLocation1" == (response.json().get("user_location"))
#
#     def test_get_new_kakao_user_data(self):
#         response = self.client.get(
#             "/api/v1/get-kakao-user", json={"user_name": "NewUser1"}
#         )
#
#         assert 200 == (response.status_code)
#         assert not None == (response.json())
#         assert "0800" == (response.json().get("user_time"))
#         assert "NewLocation1" == (response.json().get("user_location"))
#
#     def test_get_existing_kakao_user_data_0(self):
#         response = self.client.get(
#             "/api/v1/get-kakao-user", json={"user_name": "TestUser0"}
#         )
#
#         assert 200 == (response.status_code)
#         assert not None == (response.json())
#         assert "1000" == (response.json().get("user_time"))
#         assert "TestLocation0" == (response.json().get("user_location"))
#         assert True == (response.json().get("is_active"))
#
#     def test_edit_user_location(self):
#         response = self.client.put(
#             "/api/v1/edit-user-location",
#             json={"user_name": "NewUser1", "user_location": "NewLocation2"},
#         )
#
#         assert 200 == (response.status_code)
#         assert not None == (response.json())
#         assert not "NewLocation1" == (response.json().get("user_location"))
#         assert "NewLocation2" == (response.json().get("user_location"))
#
#     def test_edit_user_time(self):
#         response = self.client.put(
#             "/api/v1/edit-user-time",
#             json={"user_name": "NewUser1", "user_time": "1200"},
#         )
#
#         assert 200 == (response.status_code)
#         assert not None == (response.json())
#         assert not "0800" == (response.json().get("user_time"))
#         assert "1200" == (response.json().get("user_time"))
#
#     def test_get_kakao_users(self):
#         response = self.client.get("/api/v1/get-kakao-users")
#
#         assert 200 == (response.status_code)
#         assert not None == (response.json())
#
#     # @pytest.mark.skip(reason="")
#     def test_delete_kakao_user(self):
#         before_delete = self.client.get("/api/v1/get-kakao-users")
#
#         assert 3 == (len(before_delete.json()))
#
#         response = self.client.delete(
#             "/api/v1/delete-kakao-user", json={"user_name": "NewUser1"}
#         )
#
#         assert 200 == (response.status_code)
#         assert "User successfully deleted." == (response.json())
#
#         after_delete = self.client.get("/api/v1/get-kakao-users")
#
#         assert 2 == (len(after_delete.json()))
