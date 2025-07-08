from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.user import UserPaginationResponse
from app.lib.specifications import ILikeSpecification, InListSpecification, apply_filter_specifications, apply_order_by_specifications
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

    query = apply_filter_specifications(model=User, query=query, specifications=filters.to_specifications())

    query = apply_order_by_specifications(model=User, query=query, specifications=filters.to_order_by_specifications())

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
