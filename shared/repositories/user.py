from typing import Sequence

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.models.user import User


async def create_user(
        session: AsyncSession,
        user_id: int,
        name: str,
        gold: int,
    **kwargs,
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
        guild_id=None,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user(
        session: AsyncSession,
        user_id: int,
        name: str | None = None,
        gold: int | None = None,
        experience: int | None = None,
        rating: int | None = None,
        containers: int | None = None,
        guild_id: int | None = None,
        leaving_guild: bool = False,
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
    :param guild_id: id гильдии, которую необходимо добавить пользователю
    :param leaving_guild: Флаг, сообщающий о том, что пользователю необходимо удалить гильдию
    :return: Пользователь с обновленными данными
    """
    user = await get_user_by_foreign_id(session=session, user_id=user_id)
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
    if guild_id:
        user.guild_id = guild_id
    if leaving_guild:
        user.guild_id = None
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_foreign_id(
        session: AsyncSession,
        user_id: int,
) -> User:
    """
    Получить Пользователя на основе id из внешнего сервиса

    :param session: Сессия базы данных
    :param user_id: id пользователя из внешней базы данных
    :return: Пользователь, извлеченный из базы данных
    """
    exception = ValueError("User were not found")
    stmt = select(User).where(User.user_id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise exception
    return user


async def get_users_rating(
        session: AsyncSession,
        gold: bool = False,
        experience: bool = False,
        containers: bool = False,
) -> Sequence[User]:
    """
    Получить рейтинг пользователей на основе заданного параметра.
    Если ни один параметр не задан, сортировка строится на основе рейтинга

    :param session: Сессия базы данных
    :param gold: Если требуется рейтинг на основе золота
    :param experience: Если требуется рейтинг на основе опыта
    :param containers: Если требуется рейтинг на основе открытых контейнеров
    :return: Возвращает последовательность пользователей, отсортированных по заданному критерию
    """
    if gold:
        stmt = select(User).order_by(desc(User.gold))
    elif experience:
        stmt = select(User).order_by(desc(User.experience))
    elif containers:
        stmt = select(User).order_by(desc(User.containers))
    else:
        stmt = select(User).order_by(desc(User.rating))
    result = await session.execute(stmt)
    users = result.scalars().all()
    return users
