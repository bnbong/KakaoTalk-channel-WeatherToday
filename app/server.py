from fastapi import FastAPI

from db.database import engine

from api import routing
from db import models

from fastapi import FastAPI

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(routing.router, prefix='/api/v1')
