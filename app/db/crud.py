from sqlalchemy.orm import Session

from . import models, schemas

import os


def get_kakao_user(db: Session, user_name: str):
    return db.query(models.KakaoChannelUser).filter(models.KakaoChannelUser.user_name == user_name).first()

def get_kakao_users(db: Session):
    return db.query(models.KakaoChannelUser).all()

def create_kakao_user(db: Session, user: schemas.KakaoUserCreate):
    new_user = models.KakaoChannelUser(user_name=user.user_name, user_time=user.user_time, user_location_first=user.user_location_first, user_location_second=user.user_location_second, user_location_third=user.user_location_third)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def edit_user_location(db: Session, data: schemas.KakaoGetUser):
    selected_user = db.query(models.KakaoChannelUser).filter(models.KakaoChannelUser.user_name == data.user_name).first()
    
    selected_user.user_location_first = data.user_location_first
    selected_user.user_location_second = data.user_location_second
    selected_user.user_location_third = data.user_location_third

    db.commit()
    db.refresh(selected_user)

    return selected_user