from fastapi import FastAPI
from app.api import user_router
from app.database.database import init_db

app = FastAPI(
    lifespan=init_db
)

app.include_router(user_router)
