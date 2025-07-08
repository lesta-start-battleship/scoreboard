from broker.schemas.match.random import MatchRandomDTO


class MatchGuildWarDTO(MatchRandomDTO):
    guild_war_id: int
