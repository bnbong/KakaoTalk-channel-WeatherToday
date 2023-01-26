from sqlalchemy.orm import Session

from . import models, schemas


def get_kakao_user(db: Session, user_name: str):
    return db.query(models.KakaoChannelUser).filter(models.KakaoChannelUser.user_name == user_name).first()

def get_kakao_users(db: Session):
    return db.query(models.KakaoChannelUser).all()

def create_kakao_user(db: Session, data: schemas.KakaoUser):
    new_user = models.KakaoChannelUser(user_name=data.user_name, user_time=data.user_time, user_location=data.user_location)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return new_user

def edit_user_location(db: Session, data: schemas.KakaoGetUser):
    selected_user = db.query(models.KakaoChannelUser).filter(models.KakaoChannelUser.user_name == data.user_name).first()
    
    selected_user.user_location = data.user_location

    db.commit()
    db.refresh(selected_user)
    db.close()

    return selected_user

def edit_user_time(db: Session, data: schemas.KakaoGetUser):
    selected_user = db.query(models.KakaoChannelUser).filter(models.KakaoChannelUser.user_name == data.user_name).first()

    selected_user.user_time = data.user_time

    db.commit()
    db.refresh(selected_user)
    db.close()

    return selected_user

def delete_kakao_user(db: Session, data: schemas.KakaoGetUser):
    selected_user = db.query(models.KakaoChannelUser).filter(models.KakaoChannelUser.user_name == data.user_name).first()

    db.delete(selected_user)
    db.commit()
    db.close()

    return "User successfully deleted."