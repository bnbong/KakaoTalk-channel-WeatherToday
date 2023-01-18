from fastapi import FastAPI

from .db.database import engine

from .api import routing
from .db import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routing.router, prefix='/api/v1')
