from pydantic import BaseModel, Field


class MatchBaseDTO(BaseModel):
    winner_match_id: int = Field(..., alias="winner_id")
    loser_match_id: int = Field(..., alias="loser_id")
    match_id: str
    match_type: str
