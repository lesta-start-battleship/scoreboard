from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from shared.config.preferences import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT


def get_db_url():
    url: PostgresDsn = PostgresDsn(
        f"postgresql+asyncpg://"
        f"{DB_USER}:"
        f"{DB_PASSWORD}@"
        f"{DB_HOST}:"
        f"{DB_PORT}/"
        f"{DB_NAME}"
    )
    return str(url)


DATABASE_URL = get_db_url()

engine = create_async_engine(url=DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)
