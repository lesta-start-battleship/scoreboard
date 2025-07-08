from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped

from shared.database.models.base import Base
if TYPE_CHECKING:
    from shared.database.models.war_result import WarResult
    from shared.database.models.user import User


class Guild(Base):
    __tablename__ = "guild"

    guild_id: Mapped[int] = mapped_column(primary_key=True)
    tag: Mapped[str]
    players: Mapped[int]
    wins: Mapped[int]

    war_results: Mapped[list["WarResult"]] = relationship(
        "WarResult", back_populates="guild"
    )
    users: Mapped[list["User"]] = relationship("User", back_populates="guild")
