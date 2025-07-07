from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.user import UserPaginationResponse
from app.schemas.pagination import PaginationRequest
from app.schemas.user import UserFilterRequest, UserSchema
from shared.database.models.user import User


async def get_users(
    db: AsyncSession,
    pagination: PaginationRequest,
    filters: UserFilterRequest,
) -> UserPaginationResponse:
    # Define rank expressions
    gold_rank = func.row_number().over(order_by=User.gold.desc()).label("gold_rating_pos")
    exp_rank = func.row_number().over(order_by=User.experience.desc()).label("exp_rating_pos")
    rating_rank = func.row_number().over(order_by=User.rating.desc()).label("rating_rating_pos")
    chests_rank = func.row_number().over(order_by=User.containers.desc()).label("chests_opened_pos")

    # Base query with rankings
    query = select(
        User,
        gold_rank,
        exp_rank,
        rating_rank,
        chests_rank
    )
    
    # Apply filters
    if filters.ids:
        query = query.where(User.id.in_(filters.ids))

    if filters.name_ilike:
        query = query.where(User.name.ilike(f"%{filters.name_ilike}%"))

    # Apply ordering
    if filters.order_by_gold:
        order = User.gold.asc() if filters.order_by_gold == "asc" else User.gold.desc()
        query = query.order_by(order)

    if filters.order_by_experience:
        order = User.experience.asc() if filters.order_by_experience == "asc" else User.experience.desc()
        query = query.order_by(order)

    if filters.order_by_rating:
        order = User.rating.asc() if filters.order_by_rating == "asc" else User.rating.desc()
        query = query.order_by(order)

    if filters.order_by_chests_opened:
        order = User.containers.asc() if filters.order_by_chests_opened == "asc" else User.containers.desc()
        query = query.order_by(order)

    # Count total items
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Apply pagination
    query = query.offset(pagination.page * pagination.limit).limit(pagination.limit)

    # Execute query
    result = await db.execute(query)
    rows = result.all()

    # Convert rows to schema
    user_schemas = [
        UserSchema.model_validate(user).model_copy(update={
            "gold_rating_pos": gold_pos,
            "exp_rating_pos": exp_pos,
            "rating_rating_pos": rating_pos,
            "chests_opened_pos": chests_pos,
        })
        for user, gold_pos, exp_pos, rating_pos, chests_pos in rows
    ]

    return UserPaginationResponse(
        items=user_schemas,
        total_items=total or 0,
        total_pages=(total or 0 + pagination.limit - 1) // pagination.limit,
    )
