from enum import StrEnum

from logging import getLogger
from typing import Any, TypeVar

from sqlalchemy import ColumnClause, Select, column
from sqlalchemy.orm import DeclarativeBase, InstrumentedAttribute

from .exceptions.filter import FilterGroupAlreadyInUseException
from app.schemas.bases import BaseSchema


class OrderByType(StrEnum):
    """
    Enum for order by types.
    """
    ASC = "asc"
    DESC = "desc"

    def __str__(self):
        return str(self.value)
    

class FilterType(StrEnum):
    """Filter type."""

    eq = "eq"
    """Equals."""
    ne = "ne"
    """Not equals."""
    in_list = "in_list"
    """In list."""
    not_in_list = "not_in_list"
    """Not in list."""
    gt = "gt"
    """Greater than."""
    ge = "ge"
    """Greater than or equal."""
    lt = "lt"
    """Less than."""
    le = "le"
    """Less than or equal."""
    like = "like"
    """Like."""
    ilike = "ilike"
    """Case-insensitive like."""
    order_by = "order_by"
    """Order by (ASC or DESC)."""
    skip = "skip"
    """Skip auto-generated filter."""
    func = "func"
    """Function filter."""

"""Filtration utilities."""


logger = getLogger(__name__)

_SelectType = TypeVar("_SelectType", bound=Any)


def add_filters_to_query(
    query: Select[_SelectType],
    table: type[DeclarativeBase],
    body: BaseSchema,
    *,
    include_order_by: bool = True,
) -> Select[_SelectType]:
    """Add filter to query.

    Args:
        query (GenerativeSelect): Query to filter.
        table (type[AbstractModel]): Table to filter.
        body (BaseSchema): Schema to filter.
        include_order_by (bool): Include order by filters.

    Returns:
        Select[_SelectType]: Filtered query.
    """
    groups = set[str]()

    for field_name, field in body.model_fields.items():
        field_value = getattr(body, field_name)
        if field_value is None:
            continue
        extra: dict[str, Any]
        if callable(field.json_schema_extra):
            logger.warning(
                "Filter schema extra for field %s.%s is not a dict, but a callable",
                body.__class__.__name__,
                field_name,
            )
            continue
        if field.json_schema_extra is not None:
            extra = field.json_schema_extra
        else:
            extra = field._inititial_kwargs if hasattr(field, "_inititial_kwargs") else {} # type: ignore[assignment]
        table_column: str = extra.get("table_column", field_name)  # type: ignore[assignment]
        filter_type: FilterType = extra.get("filter_type", FilterType.eq)  # type: ignore[assignment]
        # Check if filter group is already in use, if set
        filter_group: str | None = extra.get("group", None)  # type: ignore[assignment]
        if filter_group is not None:
            if filter_group in groups:
                raise FilterGroupAlreadyInUseException(group=filter_group)
            groups.add(filter_group)
        # Skip filters
        if filter_type == FilterType.skip:
            logger.debug("Skipping filter by %s with %s and %s", table_column, filter_type, field_value)
            continue

        logger.debug("Filtering by %s with %s and %s", table_column, filter_type, field_value)
        # Replace special characters for LIKE and ILIKE filters
        # and add % to the beginning and the end of the string
        # to make it work like a wildcard
        # https://www.postgresql.org/docs/current/functions-matching.html
        if filter_type in (FilterType.like, FilterType.ilike):
            field_value = field_value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_").replace("~", "\\~")
            field_value = f"%{field_value}%"
        # Get column object
        table_column_obj: InstrumentedAttribute[Any] | ColumnClause[Any]
        current_model = table
        for col in table_column.split("."):
            table_column_obj = getattr(current_model, col, column(table_column))

            if hasattr(table_column_obj, "property") and hasattr(table_column_obj.property, "mapper"):
                current_model = table_column_obj.property.mapper.class_
            else:
                break
        # Add filter to query
        match filter_type:
            case FilterType.eq:
                query = query.filter(table_column_obj == field_value) # type: ignore[operator]
            case FilterType.ne:
                query = query.filter(table_column_obj != field_value) # type: ignore[operator]
            case FilterType.in_list:
                query = query.filter(table_column_obj.in_(field_value))
            case FilterType.not_in_list:
                query = query.filter(table_column_obj.not_in(field_value))
            case FilterType.gt:
                query = query.filter(table_column_obj > field_value) # type: ignore[operator]
            case FilterType.ge:
                query = query.filter(table_column_obj >= field_value) # type: ignore[operator]
            case FilterType.lt: 
                query = query.filter(table_column_obj < field_value) # type: ignore[operator]
            case FilterType.le:
                query = query.filter(table_column_obj <= field_value) # type: ignore[operator]
            case FilterType.like:
                query = query.filter(table_column_obj.like(field_value))
            case FilterType.ilike:
                query = query.filter(table_column_obj.ilike(field_value))
            case FilterType.order_by:
                if include_order_by:
                    query = query.order_by(
                        table_column_obj.asc() if field_value == OrderByType.ASC else table_column_obj.desc()
                    )
            case FilterType.func:
                func = extra.get("filter_func")
                if func is None:
                    raise ValueError("Filter function is not defined")
                query = func(query, table_column_obj, field_value)  # type: ignore[operator]
            case _:
                raise NotImplementedError

    logger.debug("Filtered query: %s", query)
    return query


def inclusion_filter(
    query: "Select[_SelectType]", column: "InstrumentedAttribute[Any]", value: bool
) -> "Select[_SelectType]":
    """Inclusion filter.

    Args:
        query (Select[_SelectType]): Query.
        column (InstrumentedAttribute): Column to filter.
        value (bool): Value to filter.

    Returns:
        Select[_SelectType]: Filtered query.
    """
    return query.filter(column.is_not(None) if value else column.is_(None))