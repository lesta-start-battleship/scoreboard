from uuid import UUID
from pydantic import Field
from app.lib.filter import FilterType, OrderByType
from app.lib.specifications import BaseSpecification, ILikeSpecification, InListSpecification, OrderBySpecification
from app.lib.wrap_field import DELETED_INCLUSION_FILTER, ORDER_BY_FILTER, BaseField
from app.schemas.bases import BaseFilterSchema, BaseSchema
from app.schemas.pagination import PaginationResponse


class UserSchema(BaseSchema):
    """Schema for user data."""
    
    id: UUID = Field(..., description="Unique identifier of the user")
    name: str = Field(..., description="Name of the user")
    gold: int = Field(..., description="Amount of gold the user has")
    gold_rating_pos: int = Field(..., description="User's position in the gold rating")
    experience: int = Field(..., description="Amount of experience the user has")
    exp_rating_pos: int = Field(..., description="User's position in the experience rating")
    rating: int = Field(..., description="User's rating value")
    rating_rating_pos: int = Field(..., description="User's position in the rating ranking")
    chests_opened: int = Field(..., description="Number of chests opened by the user")
    chests_opened_pos: int = Field(..., description="User's position in the chests opened ranking")


class UserPaginationResponse(PaginationResponse[UserSchema]):
    """Schema for paginated user data response."""

class UserFilterRequest(BaseFilterSchema):
    """Schema for filtering user data."""
    
    ids: list[UUID] | None = BaseField(default=None, description="User IDs to filter users by", filter_type=FilterType.in_list, table_column="id")

    name_ilike: str | None = BaseField(default=None, description="User name", filter_type=FilterType.ilike, table_column="name")

    order_by_gold: OrderByType | None = ORDER_BY_FILTER(table_column="gold")
    order_by_experience: OrderByType | None = ORDER_BY_FILTER(table_column="experience")
    order_by_rating: OrderByType | None = ORDER_BY_FILTER(table_column="rating")
    order_by_chests_opened: OrderByType | None = ORDER_BY_FILTER(table_column="containers")

    is_deleted: bool | None = DELETED_INCLUSION_FILTER

    def to_specifications(self) -> list[BaseSpecification]:
        return list(
            filter(
                None,
                [
                    InListSpecification(field="id", value=self.ids) if self.ids else None,
                    ILikeSpecification(field="name", value=self.name_ilike) if self.name_ilike else None,
                ],
            )
        )
    
    def to_order_by_specifications(self) -> list[OrderBySpecification]:
        return list(
            filter(
                None,
                [
                    OrderBySpecification(field="gold", type=self.order_by_gold) if self.order_by_gold else None,
                    OrderBySpecification(field="experience", type=self.order_by_experience) if self.order_by_experience else None,
                    OrderBySpecification(field="rating", type=self.order_by_rating) if self.order_by_rating else None,
                    OrderBySpecification(field="chests_opened", type=self.order_by_chests_opened) if self.order_by_chests_opened else None,
                ],
            )
        )