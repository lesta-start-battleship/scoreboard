from fastapi import APIRouter
from app.dependencies import DatabaseDependency
from app.schemas.war_result import WarResultFilterRequest, WarResultPaginationResponse
from app.schemas.pagination import PaginationRequest
from app.config.telemetry import get_tracer
from pyfa_converter_v2 import QueryDepends
from app.services.war_result import read as war_result_service

router = APIRouter(prefix="/war-results", tags=["war-results"])
tracer = get_tracer(__name__)

@router.get("/", response_model=WarResultPaginationResponse)
async def get_war_results(
    db: DatabaseDependency,
    pagination: PaginationRequest = QueryDepends(PaginationRequest),
    filters: WarResultFilterRequest = QueryDepends(WarResultFilterRequest),
) -> WarResultPaginationResponse:
    """
    Get a paginated list of war results.
    """
    with tracer.start_as_current_span("get_war_results_api") as span:
        span.set_attribute("pagination.page", pagination.page)
        span.set_attribute("pagination.limit", pagination.limit)
        return await war_result_service.get_war_results(db, pagination, filters)
