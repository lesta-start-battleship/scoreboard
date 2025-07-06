from pydantic import BaseModel

class GuildMemberChangeDTO(BaseModel):
    guild_id: int
    user_id: int
    user_amount: int