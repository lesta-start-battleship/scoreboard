from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped

from shared.database.models.base import Base

if TYPE_CHECKING:
    from shared.database.models.war_result import WarResult
    from shared.database.models.user import User


class Guild(Base):
    __tablename__ = "guild"

    guild_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    tag: Mapped[str]
    players: Mapped[int]
    wins: Mapped[int]

    war_results_attacker: Mapped[list["WarResult"]] = relationship(
        "WarResult", foreign_keys="[WarResult.attacker_id]", back_populates="attacker"
    )
    war_results_defender: Mapped[list["WarResult"]] = relationship(
        "WarResult", foreign_keys="[WarResult.defender_id]", back_populates="defender"
    )
    users: Mapped[list["User"]] = relationship("User", back_populates="guild")
