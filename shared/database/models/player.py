from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.attributes import Mapped

from shared.database.models.base import Base


class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int]
    name: Mapped[str] = mapped_column(unique=True)
    gold: Mapped[int]
    experience: Mapped[int]
    rating: Mapped[int]
    containers: Mapped[int]

