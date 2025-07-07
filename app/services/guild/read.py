from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.guild import GuildPaginationResponse, GuildFilterRequest, GuildSchema
from shared.database.models.guild import Guild
from app.schemas.pagination import PaginationRequest


async def get_guilds(
    db: AsyncSession,
    pagination: PaginationRequest,
    filters: GuildFilterRequest,
) -> GuildPaginationResponse:
    # Rank expressions
    players_rank = func.row_number().over(order_by=Guild.players.desc()).label("players_pos")
    wins_rank = func.row_number().over(order_by=Guild.wins.desc()).label("wins_pos")

    # Base query
    query = select(Guild, players_rank, wins_rank)

    # Apply filters
    if filters.ids:
        query = query.where(Guild.id.in_(filters.ids))

    if filters.tag_ilike:
        query = query.where(Guild.tag.ilike(f"%{filters.tag_ilike}%"))

    """
    if filters.is_deleted is not None:
        if filters.is_deleted:
            query = query.where(Guild.deleted_at.is_not(None))
        else:
            query = query.where(Guild.deleted_at.is_(None))
    """
            
    # Apply ordering
    if filters.order_by_players:
        order = Guild.players.asc() if filters.order_by_players == "asc" else Guild.players.desc()
        query = query.order_by(order)

    if filters.order_by_wins:
        order = Guild.wins.asc() if filters.order_by_wins == "asc" else Guild.wins.desc()
        query = query.order_by(order)

    # Count total items
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Pagination
    query = query.offset(pagination.page * pagination.limit).limit(pagination.limit)

    # Execute
    result = await db.execute(query)
    rows = result.all()

    # Transform rows
    guild_schemas = [
        GuildSchema.model_validate(guild).model_copy(update={
            "players_pos": players_pos,
            "wins_pos": wins_pos,
        })
        for guild, players_pos, wins_pos in rows
    ]

    return GuildPaginationResponse(
        items=guild_schemas,
        total_items=total or 0,
        total_pages=(total or 0 + pagination.limit - 1) // pagination.limit,
    )
