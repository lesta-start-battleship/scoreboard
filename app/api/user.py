from fastapi import APIRouter
from app.dependencies import DatabaseDependency
from app.schemas.pagination import PaginationRequest
from app.schemas.user import UserFilterRequest, UserPaginationResponse
from pyfa_converter_v2 import QueryDepends
from app.services import user as user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=UserPaginationResponse)
async def get_users(
    db: DatabaseDependency,
    pagination: PaginationRequest = QueryDepends(PaginationRequest),
    filters: UserFilterRequest = QueryDepends(UserFilterRequest),
) -> UserPaginationResponse:
    """
    Get a paginated list of users.
    """
    return await user_service.get_users(db, pagination, filters)
