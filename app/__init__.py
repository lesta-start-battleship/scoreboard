import logging
from fastapi import FastAPI
from app.api import router as default_router
from app.config.telemetry import setup_telemetry, instrument_app

# Setup OpenTelemetry tracing
setup_telemetry(app_name="scoreboard", app_version="1.0.0")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title="Scoreboard API",
    description="API for managing scoreboard data",
    generate_unique_id_function=lambda route: route.name,
    version="1.0.0",
)

# Instrument the app with OpenTelemetry
instrument_app(app)

app.include_router(default_router)