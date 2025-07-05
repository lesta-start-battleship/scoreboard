from fastapi import FastAPI
from app.api import user_router
from app.database.database import lifespan

app = FastAPI(
    lifespan=lifespan,
    title="Scoreboard API",
    description="API for managing scoreboard data",
    version="1.0.0",
    
)

app.include_router(user_router)
