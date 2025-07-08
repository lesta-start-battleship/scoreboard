"""Multisort alorithm implementation."""

from operator import attrgetter

from app.lib.filter import OrderByType
from app.lib.specifications import OrderBySpecification



def multisorted[T](list_to_sort: list[T], specifications: list[OrderBySpecification]) -> list[T]:
    """Sort an iterable by multiple specifications.

    Args:
        list_to_sort (list[T]): An iterable to sort.
        specifications (list[OrderBySpecification]): A list of specifications to sort by.

    Returns:
        Iterable[T]: The sorted iterable.

    """
    iterable = list_to_sort

    for specification in specifications:
        iterable = sorted(
            iterable,
            key=attrgetter(specification.field),
            reverse=specification.type == OrderByType.DESC,
        )

    return iterable