from enum import Enum


class MatchType(str, Enum):
    RANDOM = "random"
    RANKED = "ranked"
    CUSTOM = "custom"
    GUILD_WAR_MATCH = "guild_war_match"