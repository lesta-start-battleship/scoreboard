from broker.schemas.match.match_experience import MatchExperienceDTO
from broker.schemas.match.random import MatchRandomDTO


class MatchCustomDTO(MatchRandomDTO):
    experience: MatchExperienceDTO = MatchExperienceDTO(winner_gain=0, loser_gain=0)
