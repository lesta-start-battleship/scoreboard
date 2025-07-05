from pydantic import BaseModel

class Currencies(BaseModel):
    gold: int
    guild_rage: int