from uuid import UUID
from pydantic import Field
from app.lib.filter import FilterType, OrderByType
from app.lib.wrap_field import DELETED_INCLUSION_FILTER, ORDER_BY_FILTER, BaseField
from app.schemas.bases import BaseSchema
from app.schemas.pagination import PaginationResponse


class GuildSchema(BaseSchema):
    """Schema for user data."""
    
    id: UUID = Field(..., description="Unique identifier of the user")
    tag: str = Field(..., description="Tag of the guild")
    players: int = Field(..., description="Number of players in the guild")
    playes_rating_pos: int = Field(..., description="Guild's position in the players rating")
    wins: int = Field(..., description="Number of wins by the guild")
    wins_rating_pos: int = Field(..., description="Guild's position in the wins rating")


class GuildPaginationResponse(PaginationResponse[GuildSchema]):
    """Schema for paginated user data response."""

class GuildFilterRequest(BaseSchema):
    """Schema for filtering user data."""
    
    ids: list[UUID] | None = BaseField(default=None, description="Guild IDs to filter users by", filter_type=FilterType.in_list, table_column="id")

    tag_ilike: str | None = BaseField(default=None, description="Guild tag ilike", filter_type=FilterType.ilike, table_column="tag")
    order_by_players: OrderByType | None = ORDER_BY_FILTER(table_column="players")
    order_by_wins: OrderByType | None = ORDER_BY_FILTER(table_column="wins")

    is_deleted: bool | None = DELETED_INCLUSION_FILTER