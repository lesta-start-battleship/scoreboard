from typing import Sequence

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.models.guild import Guild


async def create_guild(
    session: AsyncSession,
    guild_id: int,
    tag: str,
    players: int = 1,
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


async def update_guild(
    session: AsyncSession,
    guild_id: int,
    tag: str | None = None,
    players: int | None = None,
    wins: int | None = None,
) -> Guild:
    """
    Обновить данные гильдии. Возможно обновление одного и более параметров.
    Параметры, обновление которых не требуется, можно не указывать


    :param session: Сессия базы данных
    :param guild_id: id гильдии
    :param tag: Новый тег гильдии
    :param players: Новое количество игроков гильдии
    :param wins: Количество добавленных побед
    :return: Объект Гильдия с обновленными данными
    """
    guild: Guild | None = await session.get(Guild, guild_id)
    if guild is None:
        raise ValueError("Guild were not found")
    if tag:
        guild.tag = tag
    if players:
        guild.players = players
    if wins:
        guild.wins += wins
    await session.commit()
    await session.refresh(guild)
    return guild


async def get_guilds_rating(
    session: AsyncSession, players: bool = False
) -> Sequence[Guild]:
    """
    Получить рейтинг пользователя на основе заданного параметра.
    Если ни один параметр не задан, сортировка строится на основе количества побед

    :param session: Сессия базы данных
    :param players: Если требуется рейтинг на основе количества игроков
    :return: Последовательность Гильдий, отсортированных по заданному критерию
    """
    if players:
        stmt = select(Guild).order_by(desc(Guild.players))
    else:
        stmt = select(Guild).order_by(desc(Guild.wins))
    result = await session.execute(stmt)
    guilds = result.scalars().all()
    return guilds


async def delete_guild(session: AsyncSession, guild_id: int):
    """
    Удалить гильдию из базы данных

    :param session: Сессия базы данных
    :param guild_id: id гильдии
    :return: True в случае успешного удаления
    """
    guild: Guild | None = await session.get(Guild, guild_id)
    if guild is None:
        raise ValueError("Guild were not found")
    await session.delete(guild)
    await session.commit()
    return True
