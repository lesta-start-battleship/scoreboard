from fastapi import FastAPI

app = FastAPI(
    title="Scoreboard API",
    description="API for managing scoreboard data",
    generate_unique_id_function=lambda route: route.name,
    version="1.0.0",
)
