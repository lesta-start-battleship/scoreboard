from pydantic import BaseModel

class GuildDeleteDTO(BaseModel):
    guild_id: int