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
