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
        print(response.status_code)
        print(response.json())
