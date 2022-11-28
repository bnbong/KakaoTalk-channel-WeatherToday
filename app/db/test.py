class TestDatabase():
    from .test_session_maker import client, TestingSessionLocal
    from . import models, schemas, crud


    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_could_fetch_database(self):
        query = self.TestingSessionLocal().query(self.models.KakaoChannelUser).first()

        print(query)

    def test_could_add_new_kakao_user(self):
        response = self.client.post('/api/v1/create_kakao_user', json={"user_name":"TestUser", "user_time":"0630", "user_location_first":"TestLocation1"})
        
        assert 400 == (response.status_code)
        assert "User already exists." == (response.json().get('detail'))

    def test_could_get_kakao_user(self):
        response = self.client.get('/api/v1/get_kakao_user', json={"user_name":"TestUser"})
        json_response = response.json()

        assert 200 == (response.status_code)
        assert "TestUser" == (json_response.get('user_name'))
        assert "TestLocation1" == (json_response.get('user_location_first'))
        assert None == (json_response.get('user_location_second'))
        assert None == (json_response.get('user_location_third'))
        assert "0630" == (json_response.get('user_time'))
        assert True == (json_response.get('is_active'))

    def test_could_change_user_location(self):
        pass

    def test_could_change_user_time(self):
        pass

