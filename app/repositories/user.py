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


async def update_user(
    session: AsyncSession,
    user_id: int,
    name: str | None = None,
    gold: int | None = None,
    experience: int | None = None,
    rating: int | None = None,
    containers: int | None = None,
) -> User:
    """
    Обновить данные пользователя. Возможно обновление одного и более параметров.
    Параметры, обновление которых не требуется, можно не указывать

    :param session: Сессия базы данных
    :param user_id: id пользователя из внешней базы данных
    :param name: Новый никнейм пользователя
    :param gold: Новый баланс золота пользователя
    :param experience: Количество добавленного опыта
    :param rating: Количество добавленного рейтинга
    :param containers: Количество добавленных контейнеров
    :return: Пользователь с обновленными данными
    """
    user = await _get_user_by_foreign_id(session=session, user_id=user_id)
    if name:
        user.name = name
    if gold:
        user.gold = gold
    if experience:
        user.experience += experience
    if rating:
        user.rating += rating
    if containers:
        user.containers += containers
    await session.commit()
    await session.refresh(user)
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
