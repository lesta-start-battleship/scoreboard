from pydantic import BaseModel


class GuildCreateDTO(BaseModel):
    guild_id: int
    tag: str
    user_amount: int
    user_owner_id: int
