import datetime

from broker.schemas.match.match_experience import MatchExperienceDTO

from pydantic import BaseModel

class MatchRandomDTO(BaseModel):
    winner_id: int
    loser_id: int
    match_id: str
    match_date: datetime
    match_type: str
    experience: MatchExperienceDTO
