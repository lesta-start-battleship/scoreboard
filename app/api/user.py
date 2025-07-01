from fastapi import APIRouter
from app.schemas.pagination import PaginationRequest
from app.schemas.user import UserFilterRequest, UserPaginationResponse
from pyfa_converter_v2 import QueryDepends

router = APIRouter()

@router.get("/users", response_model=UserPaginationResponse)
def get_users(
    pagination: PaginationRequest = QueryDepends(PaginationRequest),
    filters: UserFilterRequest = QueryDepends(UserFilterRequest),
) -> UserPaginationResponse:
    """
    Get a paginated list of users.
    """
    # TODO: Replace with actual database/service call
    return UserPaginationResponse(
        items=[],
        total_items=0,
        total_pages=0
    )
