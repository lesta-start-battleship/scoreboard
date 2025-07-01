import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config.preferences import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT
from app.database.models.base import Base

DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    host=DB_HOST,
    port=DB_PORT
)

engine = create_async_engine(url=DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def init_db(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == '__main__':
    asyncio.run(main())

