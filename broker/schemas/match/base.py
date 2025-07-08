import datetime

from pydantic import BaseModel


class MatchBaseDTO(BaseModel):
    winner_id: int
    loser_id: int
    match_id: str
    match_date: datetime
    match_type: str
