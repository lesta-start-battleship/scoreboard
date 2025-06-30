from typing import List

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped

from app.database.models.base import Base
from app.database.models.war_result import WarResult


class Guild(Base):
    __tablename__ = "guild"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guild_id: Mapped[int]
    tag: Mapped[str]
    players: Mapped[int]
    wins: Mapped[int]


    war_results: Mapped[List["WarResult"]] = relationship("WarResult", back_populates="guild")
