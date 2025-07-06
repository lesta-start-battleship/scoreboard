from sqlalchemy.ext.asyncio import AsyncSession

from app.api.user import UserPaginationResponse
from app.schemas.pagination import PaginationRequest
from app.schemas.user import UserFilterRequest


async def get_users(
    db: AsyncSession,
    pagination: PaginationRequest,
    filters: UserFilterRequest,
) -> UserPaginationResponse:
    raise NotImplementedError()