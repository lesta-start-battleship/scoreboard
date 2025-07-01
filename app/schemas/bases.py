from typing import Sequence

from pydantic import BaseModel, Field


class PaginationRequest(BaseModel):
    """Schema for pagination request parameters."""

    limit: int = Field(description="Limit of items per page", default=10, ge=1, le=100)
    page: int = Field(description="Page number", default=1, ge=1)


class PaginationResponse[_BaseSchema](BaseModel):
    """Schema for pagination response containing a list of items and pagination info."""

    items: Sequence[_BaseSchema] = Field(description="List of items")
    page: int = Field(description="Page number", default=1, ge=1)
    pages: int = Field(description="Total number of pages", default=0, ge=0)
