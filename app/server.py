from fastapi import FastAPI

from db.database import engine

from api.routing import router
from db import models


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(router, prefix='/api/v1')
