from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field
from shared.schemas.pagination import PaginationResponse


class UserSchema(BaseModel):
    """Schema for user data."""
    
    id: UUID = Field(..., description="Unique identifier of the user")
    name: str = Field(..., description="Name of the user")
    gold: int = Field(..., description="Amount of gold the user has")
    gold_rating_pos: int = Field(..., description="User's position in the gold rating")
    experience: int = Field(..., description="Amount of experience the user has")
    exp_rating_pos: int = Field(..., description="User's position in the experience rating")
    rating: int = Field(..., description="User's rating value")
    rating_rating_pos: int = Field(..., description="User's position in the rating ranking")


class UserPaginationResponse(PaginationResponse[UserSchema]):
    """Schema for paginated user data response."""

class UserFilterRequest(BaseModel):
    """Schema for filtering user data."""
    
    ids: list[UUID] | None = Field(None, description="Chat IDs to filter users by")

    name_ilike: str | None = Field(None, description="Filter users by name using case-insensitive partial match")

    order_by_gold: Literal["ASC", "DESC"] | None = Field(None, description="Order users by gold amount")
    order_by_experience: Literal["ASC", "DESC"] | None = Field(None, description="Order users by experience amount")
    order_by_rating: Literal["ASC", "DESC"] | None = Field(None, description="Order users by rating value")

    is_deleted: bool | None = Field(None, description="Filter users by deletion status")