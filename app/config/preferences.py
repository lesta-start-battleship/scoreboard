from os import getenv

from dotenv import load_dotenv

load_dotenv()

# db
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PORT = int(getenv("DB_PORT") or 5432)

OTEL_EXPORTER_OTLP_ENDPOINT: str | None = getenv("OTEL_EXPORTER_OTLP_ENDPOINT", None)