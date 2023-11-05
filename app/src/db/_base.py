# --------------------------------------------------------------------------
# Model의 기본이 되는 Base 클래스를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import object_session, Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta

Base: DeclarativeMeta = declarative_base()


class ModelBase(Base):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    @property
    def object_session(self) -> Session:
        return object_session(self)
