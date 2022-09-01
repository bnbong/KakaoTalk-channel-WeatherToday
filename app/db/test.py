class TestDatabase():
    from ..apps.test_session_maker import client, TestingSessionLocal

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_could_fetch_database(self):
        query = self.TestingSessionLocal().query(models.KakaoChannelUsers).first()

        print(query)
