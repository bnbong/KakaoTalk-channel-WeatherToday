from fastapi import FastAPI

from .apps import converter
from .db import crud, database, models, schemas
from .api import routing

from .settings import AppSettings

def create_app(app_settings: AppSettings) -> FastAPI:
    app = FastAPI()

    return app
