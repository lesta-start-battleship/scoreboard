from pydantic import BaseModel, Field


class GuildCreateDTO(BaseModel):
    guild_id: int
    tag: str
    players: int = Field(..., alias="user_amount")
    user_owner_id: int
