from broker.schemas.match.random import MatchRandomDTO
from pydantic import Field

class MatchGuildWarDTO(MatchRandomDTO):
    war_id: int = Field(..., aslias="guild_war_id")
