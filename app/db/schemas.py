from pydantic import BaseModel


class KakaoUserBase(BaseModel):
    user_id: str


class KakaoUser(KakaoUserBase):
    id: int
    user_time: str
    user_location_first: str
    user_location_second: str | None = None
    user_location_third: str | None = None

    class Config:
        orm_mode = True


class KakaoUserLocation(KakaoUserBase):
    location_first: str
    location_second: str | None = None
    location_third: str | None = None


class KakaoUserChangeTime(KakaoUserBase):
    time_to_change: str

