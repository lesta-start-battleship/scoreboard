from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.lib.specifications import apply_filter_specifications, apply_order_by_specifications
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

    query = apply_filter_specifications(model=Guild, query=query, specifications=filters.to_specifications())
    
    query = apply_order_by_specifications(model=Guild, query=query, specifications=filters.to_order_by_specifications())

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
