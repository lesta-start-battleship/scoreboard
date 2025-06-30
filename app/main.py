from fastapi import FastAPI

from app.database.database import init_db

app = FastAPI(
    lifespan=init_db
)
