from pydantic import BaseModel


class MatchRatingDTO(BaseModel):
    winner_gain: int
    loser_gain: int
