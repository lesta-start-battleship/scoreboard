from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from shared.database.database import async_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()