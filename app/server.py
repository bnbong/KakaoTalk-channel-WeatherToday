from app import app, get_db
from .db.database import engine

from .api import routing
from .db import models, schemas, crud


models.Base.metadata.create_all(bind=engine)

app.include_router(routing.router, prefix='/api/v1')
