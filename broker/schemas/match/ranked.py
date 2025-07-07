from broker.schemas.match.match_rating import MatchRatingDTO
from broker.schemas.match.random import MatchRandomDTO


class MatchRankedDTO(MatchRandomDTO):
    rating: MatchRatingDTO
