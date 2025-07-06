from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.war_result import WarResult


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
        winner=None,
    )
    session.add(war_result)
    await session.commit()
    await session.refresh(war_result)
    return war_result
