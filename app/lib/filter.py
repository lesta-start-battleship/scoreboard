from enum import StrEnum

from logging import getLogger
from typing import Any, TypeVar

from sqlalchemy import Select
from sqlalchemy.orm import InstrumentedAttribute



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