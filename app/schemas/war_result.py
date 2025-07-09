from pydantic import Field
from app.lib.filter import FilterType, OrderByType
from app.lib.specifications import (
    BaseSpecification,
    InListSpecification,
    EqualsSpecification,
    OrderBySpecification,
)
from app.lib.wrap_field import ORDER_BY_FILTER, BaseField
from app.schemas.bases import BaseFilterSchema, BaseSchema
from app.schemas.pagination import PaginationResponse


class WarResultSchema(BaseSchema):
    """Schema for war result data."""

    id: int = Field(..., description="Unique identifier of the war result")
    attacker_id: int = Field(..., description="ID of the attacking guild")
    defender_id: int = Field(..., description="ID of the defending guild")
    attacker_score: int = Field(..., description="Score achieved by the attacking guild")
    defender_score: int = Field(..., description="Score achieved by the defending guild")
    war_id: int = Field(..., description="Unique identifier of the war")
    winner_id: int = Field(..., description="ID of the winning guild")
    winner_tag: str = Field(..., description="Tag of the winning guild")
    correlation_id: int = Field(..., description="Correlation ID for tracking")


class WarResultPaginationResponse(PaginationResponse[WarResultSchema]):
    """Schema for paginated war result data response."""


class WarResultFilterRequest(BaseFilterSchema):
    """Schema for filtering war result data."""
    
    ids: list[int] | None = BaseField(
        default=None, 
        description="War result IDs to filter by", 
        filter_type=FilterType.in_list, 
        table_column="id"
    )
    
    attacker_ids: list[int] | None = BaseField(
        default=None, 
        description="Attacker guild IDs to filter by", 
        filter_type=FilterType.in_list, 
        table_column="attacker_id"
    )
    
    defender_ids: list[int] | None = BaseField(
        default=None, 
        description="Defender guild IDs to filter by", 
        filter_type=FilterType.in_list, 
        table_column="defender_id"
    )
    
    war_ids: list[int] | None = BaseField(
        default=None, 
        description="War IDs to filter by", 
        filter_type=FilterType.in_list, 
        table_column="war_id"
    )
    
    winner_id: int | None = BaseField(
        default=None, 
        description="Winner guild ID to filter by", 
        filter_type=FilterType.eq, 
        table_column="winner_id"
    )

    order_by_attacker_score: OrderByType | None = ORDER_BY_FILTER(table_column="attacker_score")
    order_by_defender_score: OrderByType | None = ORDER_BY_FILTER(table_column="defender_score")
    order_by_war_id: OrderByType | None = ORDER_BY_FILTER(table_column="war_id")

    def to_specifications(self) -> list[BaseSpecification]:
        return list(
            filter(
                None,
                [
                    InListSpecification(field="id", value=self.ids) if self.ids else None,
                    InListSpecification(field="attacker_id", value=self.attacker_ids) if self.attacker_ids else None,
                    InListSpecification(field="defender_id", value=self.defender_ids) if self.defender_ids else None,
                    InListSpecification(field="war_id", value=self.war_ids) if self.war_ids else None,
                    EqualsSpecification(field="winner_id", value=self.winner_id) if self.winner_id else None,
                ],
            )
        )
    
    def to_order_by_specifications(self) -> list[OrderBySpecification]:
        return list(
            filter(
                None,
                [
                    OrderBySpecification(field="attacker_score", type=self.order_by_attacker_score) if self.order_by_attacker_score else None,
                    OrderBySpecification(field="defender_score", type=self.order_by_defender_score) if self.order_by_defender_score else None,
                    OrderBySpecification(field="war_id", type=self.order_by_war_id) if self.order_by_war_id else None,
                ],
            )
        )
