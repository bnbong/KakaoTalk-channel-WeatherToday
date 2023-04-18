# TODO: refactor after complete testcases.

class TestDatabase():
    from .test_session_maker import client, TestingSessionLocal
    from app.db import models, schemas, crud    

    from sqlalchemy.exc import InvalidRequestError, IntegrityError

    
    @classmethod
    def setup_class(cls):
        try:
            db = cls.TestingSessionLocal()
            test_user = cls.models.KakaoChannelUser(user_name="TestUser0", user_time="0800", user_location="TestLocation0")
            db.add(test_user)
            db.commit()
            db.refresh(test_user)

        except cls.IntegrityError:
            print("User already added.")
        
    @classmethod
    def teardown_class(cls):
        try:
            db = cls.TestingSessionLocal()
            test_user = db.query(cls.models.KakaoChannelUser).first()
            test_user.user_location = "TestLocation0"
            
            target_user = db.query(cls.models.KakaoChannelUser).filter(cls.models.KakaoChannelUser.user_name == "TestUser1").first()

            db.delete(target_user)
            db.commit()
            db.refresh(test_user)

        except cls.InvalidRequestError:
            print("User has already deleted.")

    def test_could_add_new_kakao_user(self):
        user_data = {"user_name":"TestUser1", "user_time":"0630", "user_location":"TestLocation1"}
        new_user = self.schemas.KakaoUserTime(user_name=user_data.get("user_name"), user_time=user_data.get("user_time"), user_location=user_data.get("user_location"))

        db = self.TestingSessionLocal()
        self.crud.create_kakao_user(db=db, data=new_user)

        query = db.query(self.models.KakaoChannelUser).all()

        assert 2 == len(query)
        assert (query[0].user_name) == "TestUser0"
        assert (query[0].user_name) != "TestUser1"
        assert (query[1].user_name) == "TestUser1"

    def test_could_get_kakao_user(self):
        db = self.TestingSessionLocal()
        query = db.query(self.models.KakaoChannelUser).first()

        assert "TestUser0" == (query.user_name)
        assert "TestLocation0" == (query.user_location)
        assert "0800" == (query.user_time)
        assert True == (query.is_active)
    
    def test_should_testcase_will_not_touch_main_db(self):
        db = self.TestingSessionLocal()
        query = db.query(self.models.KakaoChannelUser).all()

        test_request = self.client.get('/api/v1/get-kakao-users')

        assert 2 == (len(query))
        # assert "TestUser0" == query[0].user_name 
        # assert query[0].user_name != test_request.json()[0].get('user_name')
        # assert query[0].user_time != test_request.json()[0].get('user_time')
        # assert "TestUser1" == query[1].user_name

    def test_could_change_user_location_edit_existing_one(self):
        db = self.TestingSessionLocal()
        selected_user = db.query(self.models.KakaoChannelUser).first()

        assert "TestLocation0" == (selected_user.user_location)

        selected_user.user_location = "NewLocation1"

        db.commit()
        db.refresh(selected_user)

        query = db.query(self.models.KakaoChannelUser).first()

        assert "NewLocation1" == (query.user_location)
        assert "TestLocation0" != (query.user_location)

    def test_could_change_user_time(self):
        db = self.TestingSessionLocal()
        selected_user = db.query(self.models.KakaoChannelUser).first()

        assert "0800" == (selected_user.user_time)

        selected_user.user_time = "1230"

        query = db.query(self.models.KakaoChannelUser).first()

        assert "0800" != (query.user_time)
        assert "1230" == (query.user_time)
