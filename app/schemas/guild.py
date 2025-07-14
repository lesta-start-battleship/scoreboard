from uuid import UUID
from pydantic import Field
from app.lib.filter import FilterType, OrderByType
from app.lib.specifications import (
    BaseSpecification,
    ILikeSpecification,
    InListSpecification,
)
from app.lib.wrap_field import DELETED_INCLUSION_FILTER, ORDER_BY_FILTER, BaseField
from app.schemas.bases import BaseFilterSchema, BaseSchema, OrderBySpecification
from app.schemas.pagination import PaginationResponse


class GuildSchema(BaseSchema):
    """Schema for user data."""

    id: int = Field(..., description="Unique identifier of the user")
    tag: str = Field(..., description="Tag of the guild")
    players: int = Field(..., description="Number of players in the guild")
    playes_rating_pos: int = Field(
        ..., description="Guild's position in the players rating"
    )
    wins: int = Field(..., description="Number of wins by the guild")
    wins_rating_pos: int = Field(..., description="Guild's position in the wins rating")


class GuildPaginationResponse(PaginationResponse[GuildSchema]):
    """Schema for paginated user data response."""


class GuildFilterRequest(BaseFilterSchema):
    """Schema for filtering user data."""

    ids: list[int] | None = BaseField(
        default=None,
        description="Guild IDs to filter users by",
        filter_type=FilterType.in_list,
        table_column="id",
    )

    tag_ilike: str | None = BaseField(
        default=None,
        description="Guild tag ilike",
        filter_type=FilterType.ilike,
        table_column="tag",
    )
    order_by_players: OrderByType | None = ORDER_BY_FILTER(table_column="players")
    order_by_wins: OrderByType | None = ORDER_BY_FILTER(table_column="wins")

    def to_specifications(self) -> list[BaseSpecification]:
        return list(
            filter(
                None,
                [
                    InListSpecification(
                        field="id",
                        value=self.ids,
                    )
                    if self.ids
                    else None,
                    ILikeSpecification(
                        field="tag",
                        value=self.tag_ilike,
                    )
                    if self.tag_ilike
                    else None,
                ],
            )
        )

    def to_order_by_specifications(self) -> list[OrderBySpecification]:
        return list(
            filter(
                None,
                [
                    OrderBySpecification(field="players", type=self.order_by_players)
                    if self.order_by_players
                    else None,
                    OrderBySpecification(field="wins", type=self.order_by_wins)
                    if self.order_by_wins
                    else None,
                ],
            )
        )


