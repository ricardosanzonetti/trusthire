from fastapi import FastAPI
from sqlalchemy import text

from app.api.health import router as health_router
from app.api.candidates import router as candidates_router

from app.core.base import Base
from app.core.config import settings
from app.core.database import engine

import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.include_router(health_router)
app.include_router(candidates_router)


@app.get("/db-health")
def db_health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "database": "connected"
    }