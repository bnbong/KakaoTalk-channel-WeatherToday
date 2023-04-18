from __future__ import annotations
from fastapi import FastAPI

from app.db.database import engine

from app.api.routing import router
from app.db import models
from app.settings import AppSettings


app_settings = AppSettings()
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(router, prefix='/api/v1')
