from pydantic import BaseModel


class MatchExperienceDTO(BaseModel):
    winner_gain: int
    loser_gain: int
