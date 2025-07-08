from uuid import UUID

from pydantic import BaseModel, Field


class GuildWarDTO(BaseModel):
    war_id: int = Field(..., alias="war_id")
    attacker_id: int = Field(..., alias="initiator_guild_id")
    defender_id: int = Field(..., alias="target_guild_id")
    correlation_id: UUID = Field(..., alias="correlation_id")
