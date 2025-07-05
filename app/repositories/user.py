from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.database.models.user import User


async def create_user(
    session: AsyncSession,
    user_id: int,
    name: str,
    gold: int,
) -> User:
    """
    Добавить пользователя в базу данных

    :param session: Сессия базы данных
    :param user_id: id пользователя из внешней базы данных
    :param name: Никнейм пользователя
    :param gold: Золото пользователя
    :return: Пользователь, добавленный в базу данных
    """
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


async def _get_user_by_foreign_id(
    session: AsyncSession,
    user_id: int,
) -> User:
    """
    Получить Пользователя на основе id из внешнего сервиса

    :param session: Сессия базы данных
    :param user_id: id пользователя из внешней базы данных
    :return: Пользователь, извлеченный из базы данных
    """
    exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )
    stmt = select(User).where(User.user_id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise exception
    return user
