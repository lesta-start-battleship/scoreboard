from broker.schemas.match.base import MatchBaseDTO
from broker.schemas.match.match_experience import MatchExperienceDTO


class MatchRandomDTO(MatchBaseDTO):
    experience: MatchExperienceDTO
