from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UserSchema")


@_attrs_define
class UserSchema:
    """Schema for user data.

    Attributes:
        id (UUID): Unique identifier of the user
        name (str): Name of the user
        gold (int): Amount of gold the user has
        gold_rating_pos (int): User's position in the gold rating
        experience (int): Amount of experience the user has
        exp_rating_pos (int): User's position in the experience rating
        rating (int): User's rating value
        rating_rating_pos (int): User's position in the rating ranking
        chests_opened (int): Number of chests opened by the user
        chests_opened_pos (int): User's position in the chests opened ranking
    """

    id: UUID
    name: str
    gold: int
    gold_rating_pos: int
    experience: int
    exp_rating_pos: int
    rating: int
    rating_rating_pos: int
    chests_opened: int
    chests_opened_pos: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        gold = self.gold

        gold_rating_pos = self.gold_rating_pos

        experience = self.experience

        exp_rating_pos = self.exp_rating_pos

        rating = self.rating

        rating_rating_pos = self.rating_rating_pos

        chests_opened = self.chests_opened

        chests_opened_pos = self.chests_opened_pos

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "gold": gold,
                "gold_rating_pos": gold_rating_pos,
                "experience": experience,
                "exp_rating_pos": exp_rating_pos,
                "rating": rating,
                "rating_rating_pos": rating_rating_pos,
                "chests_opened": chests_opened,
                "chests_opened_pos": chests_opened_pos,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        gold = d.pop("gold")

        gold_rating_pos = d.pop("gold_rating_pos")

        experience = d.pop("experience")

        exp_rating_pos = d.pop("exp_rating_pos")

        rating = d.pop("rating")

        rating_rating_pos = d.pop("rating_rating_pos")

        chests_opened = d.pop("chests_opened")

        chests_opened_pos = d.pop("chests_opened_pos")

        user_schema = cls(
            id=id,
            name=name,
            gold=gold,
            gold_rating_pos=gold_rating_pos,
            experience=experience,
            exp_rating_pos=exp_rating_pos,
            rating=rating,
            rating_rating_pos=rating_rating_pos,
            chests_opened=chests_opened,
            chests_opened_pos=chests_opened_pos,
        )

        user_schema.additional_properties = d
        return user_schema

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
