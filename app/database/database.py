import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from pydantic import PostgresDsn

from app.config.preferences import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT
from app.database.models.base import Base


def get_db_name() -> str:
    DATABASE_URL = PostgresDsn(
        f"postgresql+asyncpg://"
        f"{DB_USER}:"
        f"{DB_PASSWORD}@"
        f"{DB_HOST}:"
        f"{DB_PORT}/"
        f"{DB_NAME}"
    )
    return str(DATABASE_URL)


engine = create_async_engine(url=get_db_name(), echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def init_db(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(main())
