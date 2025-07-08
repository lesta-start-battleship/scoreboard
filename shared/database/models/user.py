from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped

from shared.database.models.base import Base
from shared.database.models.guild import Guild


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int]
    guild_id: Mapped[int | None] = mapped_column(ForeignKey("guild.id"), nullable=True)
    name: Mapped[str] = mapped_column(unique=True)
    gold: Mapped[int]
    experience: Mapped[int]
    rating: Mapped[int]
    containers: Mapped[int]

    guild: Mapped[Guild | None] = relationship("Guild", back_populates="users")
