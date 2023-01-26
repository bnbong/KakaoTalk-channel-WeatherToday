from pydantic import BaseModel


class KakaoUserBase(BaseModel):
    user_location: str | None = "서울특별시"


class KakaoUser(KakaoUserBase):
    user_name: str
    user_time: str | None = "0800"
    is_active: bool | None = True
    
    class Config:
        orm_mode = True

class KakaoGetUser(KakaoUserBase):
    user_name: str


class KakaoUserTime(KakaoGetUser):
    user_time: str
