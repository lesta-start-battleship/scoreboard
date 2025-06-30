import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.engine.create import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm.session import sessionmaker

from app.config.preferences import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT
from app.database.models.base import Base

DATABASE_URL = URL.create(
    drivername="postgresql",
    username=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    host=DB_HOST,
    port=DB_PORT
)

engine = create_engine(url=DATABASE_URL, echo=True)

db_session = sessionmaker(engine)


@asynccontextmanager
async def init_db(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()


async def main():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    asyncio.run(main())

