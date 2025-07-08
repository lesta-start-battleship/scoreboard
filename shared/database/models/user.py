from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped

from shared.database.models.base import Base

if TYPE_CHECKING:
    from shared.database.models.guild import Guild


class User(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    guild_id: Mapped[int | None] = mapped_column(ForeignKey("guild.guild_id"), nullable=True)
    name: Mapped[str] = mapped_column(unique=True)
    gold: Mapped[int]
    experience: Mapped[int]
    rating: Mapped[int]
    containers: Mapped[int]

    guild: Mapped[Optional["Guild"]] = relationship("Guild", back_populates="users")
