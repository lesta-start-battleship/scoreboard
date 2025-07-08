from uuid import UUID

from pydantic import BaseModel


class GuildWarResponseDTO(BaseModel):
    id_guild_attacker: int
    score_attacker: int
    id_guild_defender: int
    score_defender: int
    id_winner: int
    id_guild_war: int
    correlation_id: str
