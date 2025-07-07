from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.guild_pagination_response import GuildPaginationResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.order_by_type import OrderByType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, int] = 10,
    page: Union[Unset, int] = 1,
    ids: Union[None, Unset, list[UUID]] = UNSET,
    tag_ilike: Union[None, Unset, str] = UNSET,
    order_by_players: Union[None, OrderByType, Unset] = UNSET,
    order_by_wins: Union[None, OrderByType, Unset] = UNSET,
    is_deleted: Union[None, Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["page"] = page

    json_ids: Union[None, Unset, list[str]]
    if isinstance(ids, Unset):
        json_ids = UNSET
    elif isinstance(ids, list):
        json_ids = []
        for ids_type_0_item_data in ids:
            ids_type_0_item = str(ids_type_0_item_data)
            json_ids.append(ids_type_0_item)

    else:
        json_ids = ids
    params["ids"] = json_ids

    json_tag_ilike: Union[None, Unset, str]
    if isinstance(tag_ilike, Unset):
        json_tag_ilike = UNSET
    else:
        json_tag_ilike = tag_ilike
    params["tag_ilike"] = json_tag_ilike

    json_order_by_players: Union[None, Unset, str]
    if isinstance(order_by_players, Unset):
        json_order_by_players = UNSET
    elif isinstance(order_by_players, OrderByType):
        json_order_by_players = order_by_players.value
    else:
        json_order_by_players = order_by_players
    params["order_by_players"] = json_order_by_players

    json_order_by_wins: Union[None, Unset, str]
    if isinstance(order_by_wins, Unset):
        json_order_by_wins = UNSET
    elif isinstance(order_by_wins, OrderByType):
        json_order_by_wins = order_by_wins.value
    else:
        json_order_by_wins = order_by_wins
    params["order_by_wins"] = json_order_by_wins

    json_is_deleted: Union[None, Unset, bool]
    if isinstance(is_deleted, Unset):
        json_is_deleted = UNSET
    else:
        json_is_deleted = is_deleted
    params["is_deleted"] = json_is_deleted

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/guilds/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GuildPaginationResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = GuildPaginationResponse.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[GuildPaginationResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 10,
    page: Union[Unset, int] = 1,
    ids: Union[None, Unset, list[UUID]] = UNSET,
    tag_ilike: Union[None, Unset, str] = UNSET,
    order_by_players: Union[None, OrderByType, Unset] = UNSET,
    order_by_wins: Union[None, OrderByType, Unset] = UNSET,
    is_deleted: Union[None, Unset, bool] = UNSET,
) -> Response[Union[GuildPaginationResponse, HTTPValidationError]]:
    """Get Guilds

     Get a paginated list of users.

    Args:
        limit (Union[Unset, int]): Limit of items per page Default: 10.
        page (Union[Unset, int]): Page number Default: 1.
        ids (Union[None, Unset, list[UUID]]): Guild IDs to filter users by
        tag_ilike (Union[None, Unset, str]): Guild tag ilike
        order_by_players (Union[None, OrderByType, Unset]): Order by filter.
        order_by_wins (Union[None, OrderByType, Unset]): Order by filter.
        is_deleted (Union[None, Unset, bool]): Object deleted inclusion filter.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GuildPaginationResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        page=page,
        ids=ids,
        tag_ilike=tag_ilike,
        order_by_players=order_by_players,
        order_by_wins=order_by_wins,
        is_deleted=is_deleted,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 10,
    page: Union[Unset, int] = 1,
    ids: Union[None, Unset, list[UUID]] = UNSET,
    tag_ilike: Union[None, Unset, str] = UNSET,
    order_by_players: Union[None, OrderByType, Unset] = UNSET,
    order_by_wins: Union[None, OrderByType, Unset] = UNSET,
    is_deleted: Union[None, Unset, bool] = UNSET,
) -> Optional[Union[GuildPaginationResponse, HTTPValidationError]]:
    """Get Guilds

     Get a paginated list of users.

    Args:
        limit (Union[Unset, int]): Limit of items per page Default: 10.
        page (Union[Unset, int]): Page number Default: 1.
        ids (Union[None, Unset, list[UUID]]): Guild IDs to filter users by
        tag_ilike (Union[None, Unset, str]): Guild tag ilike
        order_by_players (Union[None, OrderByType, Unset]): Order by filter.
        order_by_wins (Union[None, OrderByType, Unset]): Order by filter.
        is_deleted (Union[None, Unset, bool]): Object deleted inclusion filter.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GuildPaginationResponse, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        limit=limit,
        page=page,
        ids=ids,
        tag_ilike=tag_ilike,
        order_by_players=order_by_players,
        order_by_wins=order_by_wins,
        is_deleted=is_deleted,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 10,
    page: Union[Unset, int] = 1,
    ids: Union[None, Unset, list[UUID]] = UNSET,
    tag_ilike: Union[None, Unset, str] = UNSET,
    order_by_players: Union[None, OrderByType, Unset] = UNSET,
    order_by_wins: Union[None, OrderByType, Unset] = UNSET,
    is_deleted: Union[None, Unset, bool] = UNSET,
) -> Response[Union[GuildPaginationResponse, HTTPValidationError]]:
    """Get Guilds

     Get a paginated list of users.

    Args:
        limit (Union[Unset, int]): Limit of items per page Default: 10.
        page (Union[Unset, int]): Page number Default: 1.
        ids (Union[None, Unset, list[UUID]]): Guild IDs to filter users by
        tag_ilike (Union[None, Unset, str]): Guild tag ilike
        order_by_players (Union[None, OrderByType, Unset]): Order by filter.
        order_by_wins (Union[None, OrderByType, Unset]): Order by filter.
        is_deleted (Union[None, Unset, bool]): Object deleted inclusion filter.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GuildPaginationResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        page=page,
        ids=ids,
        tag_ilike=tag_ilike,
        order_by_players=order_by_players,
        order_by_wins=order_by_wins,
        is_deleted=is_deleted,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 10,
    page: Union[Unset, int] = 1,
    ids: Union[None, Unset, list[UUID]] = UNSET,
    tag_ilike: Union[None, Unset, str] = UNSET,
    order_by_players: Union[None, OrderByType, Unset] = UNSET,
    order_by_wins: Union[None, OrderByType, Unset] = UNSET,
    is_deleted: Union[None, Unset, bool] = UNSET,
) -> Optional[Union[GuildPaginationResponse, HTTPValidationError]]:
    """Get Guilds

     Get a paginated list of users.

    Args:
        limit (Union[Unset, int]): Limit of items per page Default: 10.
        page (Union[Unset, int]): Page number Default: 1.
        ids (Union[None, Unset, list[UUID]]): Guild IDs to filter users by
        tag_ilike (Union[None, Unset, str]): Guild tag ilike
        order_by_players (Union[None, OrderByType, Unset]): Order by filter.
        order_by_wins (Union[None, OrderByType, Unset]): Order by filter.
        is_deleted (Union[None, Unset, bool]): Object deleted inclusion filter.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GuildPaginationResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            page=page,
            ids=ids,
            tag_ilike=tag_ilike,
            order_by_players=order_by_players,
            order_by_wins=order_by_wins,
            is_deleted=is_deleted,
        )
    ).parsed
