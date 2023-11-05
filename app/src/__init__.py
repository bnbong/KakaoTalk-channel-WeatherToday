# --------------------------------------------------------------------------
# FastAPI Application을 생성하는 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import logging

from setuptools_scm import get_version

from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.db.database import engine, Base
from src.router import router
from src.core.settings import AppSettings
from src.utils.documents import add_description_at_api_tags
from src.helper.logging import init_logger as _init_logger

__version__ = get_version(root="../..", relative_to=__file__)

logger = logging.getLogger(__name__)


def init_logger(app_settings: AppSettings) -> None:
    _init_logger(f"fastapi-backend@{__version__}", app_settings)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Application startup")
        logger.info("Create connection and setting up database")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
    finally:
        logger.info("Application shutdown")


def create_app(app_settings: AppSettings) -> FastAPI:
    app = FastAPI(
        title="Simple Backend API",
        description="Simple Backend Application using FastAPI",
        version=__version__,
        lifespan=lifespan,
    )

    app.include_router(router)

    add_description_at_api_tags(app)

    return app
