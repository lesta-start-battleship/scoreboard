from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.sql.schema import ForeignKey

from app.database.models.base import Base
from app.database.models.guild import Guild


class WarResult(Base):
    __tablename__ = "war_result"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    attacker_id: Mapped[int] = mapped_column(ForeignKey("guild.id"), nullable=False)
    defender_id: Mapped[int] = mapped_column(ForeignKey("guild.id"), nullable=False)
    attacker_score: Mapped[int]
    defender_score: Mapped[int]
    war_id: Mapped[int]
    winner_id: Mapped[int]

    guild: Mapped["Guild"] = relationship("Guild", back_populates="war_results")

