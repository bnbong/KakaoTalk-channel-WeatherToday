# 수정 필요 : test 용도로 만들어진 test.db 에 데이터가 저장되는 것이 아닌 postgresql 컨테이너에 있는 db에 값이 저장되는 것으로 보임.

class TestDatabase():
    from .test_session_maker import client, TestingSessionLocal
    from . import models, schemas, crud

    from sqlalchemy.exc import InvalidRequestError, IntegrityError


    @classmethod
    def setup_class(cls):
        try:
            db = cls.TestingSessionLocal()
            test_user = cls.models.KakaoChannelUser(user_name="TestUser0", user_time="0800", user_location_first="TestLocation0")
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
        except cls.IntegrityError:
            print("User already added.")
        
    @classmethod
    def teardown_class(cls):
        try:
            db = cls.TestingSessionLocal()
            target_user = db.query(cls.models.KakaoChannelUser).filter(cls.models.KakaoChannelUser.user_name == "TestUser1").first()
            db.delete(target_user)
            db.commit()

        except cls.InvalidRequestError:
            print("User has already deleted.")

    def test_could_add_new_kakao_user(self):
        user_data = {"user_name":"TestUser1", "user_time":"0630", "user_location_first":"TestLocation1"}
        new_user = self.schemas.KakaoUserCreate(user_name=user_data.get("user_name"), user_time=user_data.get("user_time"), user_location_first=user_data.get("user_location_first"))

        db = self.TestingSessionLocal()
        self.crud.create_kakao_user(db=db, user=new_user)

        query = db.query(self.models.KakaoChannelUser).all()

        assert 2 == len(query)
        assert (query[0].user_name) == "TestUser0"
        assert (query[0].user_name) != "TestUser1"
        assert (query[1].user_name) == "TestUser1"

    def test_could_get_kakao_user(self):
        db = self.TestingSessionLocal()
        query = db.query(self.models.KakaoChannelUser).first()

        assert "TestUser0" == (query.user_name)
        assert "TestLocation0" == (query.user_location_first)
        assert None == (query.user_location_second)
        assert None == (query.user_location_third)
        assert "0800" == (query.user_time)
        assert True == (query.is_active)
    
    def test_should_testcase_will_not_touch_main_db(self):
        pass

    def test_could_change_user_location(self):
        pass

    def test_could_change_user_time(self):
        pass

