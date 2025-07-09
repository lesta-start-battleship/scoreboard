from fastapi import APIRouter
from app.dependencies import DatabaseDependency
from app.schemas.guild import GuildFilterRequest, GuildPaginationResponse
from app.schemas.pagination import PaginationRequest
from pyfa_converter_v2 import QueryDepends
from app.services import guild as guild_service

router = APIRouter(prefix="/guilds", tags=["guild"])

@router.get("/", response_model=GuildPaginationResponse)
async def get_guilds(
    db: DatabaseDependency,
    pagination: PaginationRequest = QueryDepends(PaginationRequest),
    filters: GuildFilterRequest = QueryDepends(GuildFilterRequest),
) -> GuildPaginationResponse:
    """
    Get a paginated list of users.
    """
    return await guild_service.get_guilds(db, pagination, filters)
