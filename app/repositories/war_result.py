from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.database.models.war_result import WarResult
from app.database.models.guild import Guild


async def create_war_result(
    session: AsyncSession, attacker_id: int, defender_id: int, war_id: int
) -> WarResult:
    """
    Создать новый счётчик войны гильдий, добавив его в базу данных

    :param session: Сессия базы данных
    :param attacker_id: id атакующей гильдии
    :param defender_id: id защищающейся гильдии
    :param war_id: id войны, в рамках которой ведётся счёт
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
    )
    session.add(war_result)
    await session.commit()
    await session.refresh(war_result)
    return war_result


async def update_war_result(
    session: AsyncSession,
    war_id: int,
    attacker_score: int | None = None,
    defender_score: int | None = None,
    winner_id: int | None = None,
) -> WarResult:
    """
    Обновить данные счёта о войне гильдий

    :param session: Сессия базы данных
    :param war_id: id войны, в рамках которой ведётся счёт
    :param attacker_score: Количество добавленных очков атакующей гильдии
    :param defender_score: Количество добавленных очков защищающейся гильдии
    :param winner_id: id победившей гильдии
    :return: Объект Результаты войны с обновленными данными
    """
    exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="War result has winner, update not allow",
    )
    war_result = await get_war_result_by_foreign_id(session=session, war_id=war_id)
    if war_result.winner_id is not None:
        raise exception
    if attacker_score:
        war_result.attacker_score += attacker_score
    if defender_score:
        war_result.defender_score += defender_score
    if winner_id:
        war_result.winner_id = winner_id
    await session.commit()
    await session.refresh(war_result)
    return war_result


async def get_war_result_by_foreign_id(
    session: AsyncSession,
    war_id: int,
) -> WarResult:
    """
    Получить данные о счёте в войне гильдий на основе id из внешнего сервиса

    :param session: Сессия базы данных
    :param war_id: id войны, в рамках которой ведётся счёт
    :return: Объект Результаты войны, извлеченный из базы данных
    """
    exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="War result not found",
    )
    stmt = select(WarResult).where(WarResult.war_id == war_id)
    result = await session.execute(stmt)
    war_result = result.scalar_one_or_none()
    if war_result is None:
        raise exception
    return war_result


async def _get_winner_tag(
    session: AsyncSession,
    winner_id: int,
) -> str:
    """
    Получить тэг победившей гильдии

    :param session: Сессия базы данных
    :param winner_id: id победившей гильдии
    :return: Строка, содержащая искомый тег
    """
    stmt = select(Guild.tag).where(Guild.guild_id == winner_id)
    result = await session.execute(stmt)
    tag = result.scalar_one_or_none()
    return tag
