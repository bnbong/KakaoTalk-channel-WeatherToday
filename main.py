from __future__ import annotations

from app.db.database import engine

from app import create_app
from app.api.routing import router
from app.db import models
from app.settings import AppSettings


app_settings = AppSettings()
app = create_app(app_settings=app_settings)

models.Base.metadata.create_all(bind=engine)

app.include_router(router, prefix='/api/v1')
