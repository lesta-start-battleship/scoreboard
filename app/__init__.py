from fastapi import FastAPI
from app.api import router as default_router

app = FastAPI(
    title="Scoreboard API",
    description="API for managing scoreboard data",
    generate_unique_id_function=lambda route: route.name,
    version="1.0.0",
)
app.include_router(default_router)