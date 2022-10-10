from pydantic import BaseModel


class KakaoUserBase(BaseModel):
    user_location_first: str
    user_location_second: str | None = None
    user_location_third: str | None = None


class KakaoUser(KakaoUserBase):
    id: int
    user_name: str
    user_time: str
    is_active: bool
    
    class Config:
        orm_mode = True


class KakaoUserCreate(KakaoUserBase):
    user_name: str
    user_time: str


class KakaoUserChangeTime(KakaoUserBase):
    time_to_change: str


class KakaoUserChangeLocal():
    pass

