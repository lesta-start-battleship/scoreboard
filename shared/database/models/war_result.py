from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.sql.schema import ForeignKey

from shared.database.models.base import Base

if TYPE_CHECKING:
    from shared.database.models.guild import Guild


class WarResult(Base):
    __tablename__ = "war_result"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    attacker_id: Mapped[int] = mapped_column(ForeignKey("guild.id"), nullable=False)
    defender_id: Mapped[int] = mapped_column(ForeignKey("guild.id"), nullable=False)
    attacker_score: Mapped[int]
    defender_score: Mapped[int]
    war_id: Mapped[int]
    winner_id: Mapped[int | None]
    winner_tag: Mapped[str | None]
    loser_id: Mapped[int | None]
    loser_tag: Mapped[str | None]
    correlation_id: Mapped[int]

    guild: Mapped["Guild"] = relationship("Guild", back_populates="war_results")
    attacker: Mapped["Guild"] = relationship("Guild", foreign_keys=[attacker_id])
    defender: Mapped["Guild"] = relationship("Guild", foreign_keys=[defender_id])
