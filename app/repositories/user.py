from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.user import User


async def create_user(
    session: AsyncSession,
    user_id: int,
    name: str,
    gold: int,
) -> User:
    user = User(
        user_id=user_id,
        name=name,
        gold=gold,
        experience=0,
        rating=0,
        containers=0,
    )
    session.add(user)
    await session.commit()
    return user
