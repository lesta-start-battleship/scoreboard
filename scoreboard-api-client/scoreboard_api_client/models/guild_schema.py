from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GuildSchema")


@_attrs_define
class GuildSchema:
    """Schema for user data.

    Attributes:
        id (UUID): Unique identifier of the user
        tag (str): Tag of the guild
        players (int): Number of players in the guild
        wins (int): Number of wins by the guild
    """

    id: UUID
    tag: str
    players: int
    wins: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        tag = self.tag

        players = self.players

        wins = self.wins

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "tag": tag,
                "players": players,
                "wins": wins,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        tag = d.pop("tag")

        players = d.pop("players")

        wins = d.pop("wins")

        guild_schema = cls(
            id=id,
            tag=tag,
            players=players,
            wins=wins,
        )

        guild_schema.additional_properties = d
        return guild_schema

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
