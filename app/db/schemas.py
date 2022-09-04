from pydantic import BaseModel


class KakaoChannelUserBase(BaseModel):
    user_id: str


class KakaoChannelUser(KakaoChannelUserBase):
    id: int
    user_time: str
    user_location_first: str
    user_location_second: str | None = None
    user_location_third: str | None = None

    class Config:
        orm_mode = True


class KakaoChannelUserLocation(KakaoChannelUserBase):
    location_first: str
    location_second: str | None = None
    location_third: str | None = None


class KakaoChannelUserChangeTime(KakaoChannelUserBase):
    time_to_change: str

