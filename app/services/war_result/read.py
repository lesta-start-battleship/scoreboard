from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.lib.specifications import apply_filter_specifications, apply_order_by_specifications
from app.schemas.pagination import PaginationRequest
from app.schemas.war_result import WarResultFilterRequest, WarResultSchema, WarResultPaginationResponse
from shared.database.models.war_result import WarResult


async def get_war_results(
    db: AsyncSession,
    pagination: PaginationRequest,
    filters: WarResultFilterRequest,
) -> WarResultPaginationResponse:
    """Get paginated war results with optional filtering."""
    
    # Base query
    query = select(WarResult)

    # Apply filters
    query = apply_filter_specifications(
        model=WarResult, 
        query=query, 
        specifications=filters.to_specifications()
    )

    # Apply ordering
    query = apply_order_by_specifications(
        model=WarResult,
        query=query,
        specifications=filters.to_order_by_specifications()
    )

    # Calculate total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Apply pagination
    offset = (pagination.page - 1) * pagination.limit
    query = query.offset(offset).limit(pagination.limit)

    # Execute query
    result = await db.execute(query)
    war_results = result.scalars().all()

    # Convert to schemas
    items = [
        WarResultSchema(
            id=war_result.id,
            attacker_id=war_result.attacker_id,
            defender_id=war_result.defender_id,
            attacker_score=war_result.attacker_score,
            defender_score=war_result.defender_score,
            war_id=war_result.war_id,
            winner_id=war_result.winner_id,
            winner_tag=war_result.winner_tag,
            correlation_id=war_result.correlation_id,
        )
        for war_result in war_results
    ]

    # Calculate pagination info
    total_pages = (total or 0 + pagination.limit - 1) // pagination.limit

    return WarResultPaginationResponse(
        items=items,
        total_items=total or 0,
        total_pages=total_pages,
    )
