from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.guild import GuildFilterRequest, GuildPaginationResponse
from app.schemas.pagination import PaginationRequest


async def get_guilds(
    db: AsyncSession,
    pagination: PaginationRequest,
    filters: GuildFilterRequest,
) -> GuildPaginationResponse:
    raise NotImplementedError()