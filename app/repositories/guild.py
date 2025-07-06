from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.database.models.guild import Guild


async def create_guild(
    session: AsyncSession, guild_id: int, tag: str, players: int = 1
) -> Guild:
    """
    Добавить гильдию в базу данных

    :param session: Сессия базы данных
    :param guild_id: id гильдии из внешней базы данных
    :param tag: Тег гильдии
    :param players: Количество игроков в гильдии
    :return: Объект Гильдия, добавленный в базу данных
    """
    guild = Guild(
        guild_id=guild_id,
        tag=tag,
        players=players,
        wins=0,
    )
    session.add(guild)
    await session.commit()
    await session.refresh(guild)
    return guild


async def get_guild_by_foreign_id(
    session: AsyncSession,
    guild_id: int,
) -> Guild:
    """
    Получить гильдию на основе id из внешнего сервиса

    :param session: Сессия базы данных
    :param guild_id: id гильдии из внешней базы данных
    :return: Объект Гильдия, извлеченный из базы данных
    """
    exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Guild not found",
    )
    stmt = select(Guild).where(Guild.guild_id == guild_id)
    result = await session.execute(stmt)
    guild = result.scalar_one_or_none()
    if guild is None:
        raise exception
    return guild
