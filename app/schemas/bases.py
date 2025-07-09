from abc import ABC, abstractmethod
from typing import Any, Generator, Sequence
from pydantic import BaseModel, ConfigDict

from app.lib.specifications import BaseSpecification, OrderBySpecification


class BaseSchema(BaseModel, ABC):

    model_config = ConfigDict(from_attributes=True)

    def iterate_set_fields(self, exclude: Sequence[str] | None = None) -> Generator[tuple[str, Any], None, None]:
        """Iterate over set fields."""
        for field_name in self.model_fields_set:
            if field_name in (exclude or []):
                continue
            attr = getattr(self, field_name)
            yield field_name, attr

class BaseFilterSchema(BaseSchema, ABC):
    """Base filter schema for filtering queries."""

    @abstractmethod
    def to_specifications(self) -> list[BaseSpecification]:
        """Convert the filter schema to a list of specifications."""

    @abstractmethod
    def to_order_by_specifications(self) -> list[OrderBySpecification]:
        """Convert the filter schema to an order by specification."""