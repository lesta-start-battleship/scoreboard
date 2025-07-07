from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.user_schema import UserSchema


T = TypeVar("T", bound="UserPaginationResponse")


@_attrs_define
class UserPaginationResponse:
    """Schema for paginated user data response.

    Attributes:
        items (list['UserSchema']): List of items
        total_items (int): Total number of items
        total_pages (int): Total number of pages
    """

    items: list["UserSchema"]
    total_items: int
    total_pages: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        total_items = self.total_items

        total_pages = self.total_pages

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
                "total_items": total_items,
                "total_pages": total_pages,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_schema import UserSchema

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = UserSchema.from_dict(items_item_data)

            items.append(items_item)

        total_items = d.pop("total_items")

        total_pages = d.pop("total_pages")

        user_pagination_response = cls(
            items=items,
            total_items=total_items,
            total_pages=total_pages,
        )

        user_pagination_response.additional_properties = d
        return user_pagination_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
