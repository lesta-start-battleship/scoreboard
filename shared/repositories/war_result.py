from typing import Sequence

from sqlalchemy import select, or_, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from shared.database.models.guild import Guild
from shared.database.models.user import User
from shared.database.models.war_result import WarResult


async def create_war_result(
        session: AsyncSession,
        attacker_id: int,
        defender_id: int,
        war_id: int,
        correlation_id: int,
) -> WarResult:
    """
    Создать новый счётчик войны гильдий, добавив его в базу данных

    :param session: Сессия базы данных
    :param attacker_id: id атакующей гильдии
    :param defender_id: id защищающейся гильдии
    :param war_id: id войны, в рамках которой ведётся счёт
    :param correlation_id: uuid сообщения в kafka
    :return: Созданный и добавленный в базу данных счётчик войны гильдий
    """
    war_result = WarResult(
        attacker_id=attacker_id,
        defender_id=defender_id,
        war_id=war_id,
        attacker_score=0,
        defender_score=0,
        winner_id=None,
        winner_tag=None,
        loser_id=None,
        loser_tag=None,
        correlation_id=correlation_id,
    )
    session.add(war_result)
    await session.commit()
    await session.refresh(war_result)
    return war_result


async def update_war_result(
        session: AsyncSession,
        war_id: int,
        winner_match_id: int | None = None,
        winner_war_id: int | None = None,
        loser_war_id: int | None = None,
) -> WarResult:
    """
    Обновить данные счёта о войне гильдий

    :param session: Сессия базы данных
    :param war_id: id войны, в рамках которой ведётся счёт
    :param winner_match_id: id победившего пользователя
    :param winner_war_id: id победившей гильдии
    :param loser_war_id: id проигравшей гильдии
    :return: Объект Результаты войны с обновленными данными
    """
    exception = ValueError("War result has winner, update not allow")
    war_result: WarResult | None = await session.get(WarResult, war_id)
    if war_result.winner_id is not None:
        raise exception
    if winner_match_id:
        guilds_id = _get_attacker_defender_id(
            session=session, war_id=war_id, winner_match_id=winner_match_id
        )
        if guilds_id["winner"] == guilds_id["attacker"]:
            war_result.attacker_score += 1
        else:
            war_result.defender_score += 1
    if winner_war_id:
        war_result.winner_id = winner_war_id
        winner_tag = await _get_guild_tag(session=session, guild_id=winner_war_id)
        war_result.winner_tag = winner_tag
        war_result.loser_id = loser_war_id
        loser_tag = await _get_guild_tag(session=session, guild_id=loser_war_id)
        war_result.loser_tag = loser_tag
    await session.commit()
    await session.refresh(war_result)
    return war_result


async def get_all_war_result(session: AsyncSession) -> Sequence[WarResult]:
    """
    Получить все счёты войн гильдий

    :param session: Сессия базы данных
    :return: Последовательность объектов Результат войны
    """
    stmt = select(WarResult)
    result = await session.execute(stmt)
    war_results = result.scalars().all()
    return war_results


async def _get_guild_tag(
        session: AsyncSession,
        guild_id: int,
) -> str:
    """
    Получить тэг победившей гильдии

    :param session: Сессия базы данных
    :param guild_id: id гильдии, для которой необходим тег
    :return: Строка, содержащая искомый тег
    """
    stmt = select(Guild.tag).where(Guild.guild_id == guild_id)
    result = await session.execute(stmt)
    tag = result.scalar_one_or_none()
    return tag


async def _get_attacker_defender_id(
        session: AsyncSession, war_id: int, winner_match_id: int
) -> dict[str:int]:
    """
    Получить id атакующей, защищающейся, победившей гильдии

    :param session: Сессия базы данных
    :param war_id: id войны, в рамках которой ведётся счёт
    :param winner_match_id: id победившего пользователя
    :return: Словарь с ключами attacker, defender, winner, содержащий id соответствующих им гильдий
    """
    exception = ValueError("Winner is not in Guild")
    stmt = select(User.guild_id).where(User.user_id == winner_match_id)
    result: Result = await session.execute(stmt)
    guild_id = result.scalar_one_or_none()

    if guild_id is None:
        raise exception

    stmt = (
        select(WarResult)
        .options(
            joinedload(WarResult.attacker),
            joinedload(WarResult.defender)
        )
        .where(WarResult.war_id == war_id)
    )
    result: Result = await session.execute(stmt)
    war_result: WarResult = result.scalar_one_or_none()
    if war_result is None:
        raise ValueError("War result was not found")
    attacker = war_result.attacker.guild_id
    defender = war_result.defender.guild_id
    if guild_id not in (attacker, defender):
        raise ValueError("Winner not in this war")
    answer = {
        "attacker": attacker,
        "defender": defender,
        "winner": guild_id,
    }
    return answer
