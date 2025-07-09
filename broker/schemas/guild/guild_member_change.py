from pydantic import BaseModel, Field


class GuildMemberChangeDTO(BaseModel):
    guild_id: int
    user_id: int
    action: int
    players: int = Field(...,alias="user_amount")
