from sqlalchemy.ext.asyncio import AsyncSession

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
