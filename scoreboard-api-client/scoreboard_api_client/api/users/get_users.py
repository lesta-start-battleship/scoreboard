from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.order_by_type import OrderByType
from ...models.user_pagination_response import UserPaginationResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, int] = 10,
    page: Union[Unset, int] = 1,
    ids: Union[None, Unset, list[UUID]] = UNSET,
    name_ilike: Union[None, Unset, str] = UNSET,
    order_by_gold: Union[None, OrderByType, Unset] = UNSET,
    order_by_experience: Union[None, OrderByType, Unset] = UNSET,
    order_by_rating: Union[None, OrderByType, Unset] = UNSET,
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

    json_name_ilike: Union[None, Unset, str]
    if isinstance(name_ilike, Unset):
        json_name_ilike = UNSET
    else:
        json_name_ilike = name_ilike
    params["name_ilike"] = json_name_ilike

    json_order_by_gold: Union[None, Unset, str]
    if isinstance(order_by_gold, Unset):
        json_order_by_gold = UNSET
    elif isinstance(order_by_gold, OrderByType):
        json_order_by_gold = order_by_gold.value
    else:
        json_order_by_gold = order_by_gold
    params["order_by_gold"] = json_order_by_gold

    json_order_by_experience: Union[None, Unset, str]
    if isinstance(order_by_experience, Unset):
        json_order_by_experience = UNSET
    elif isinstance(order_by_experience, OrderByType):
        json_order_by_experience = order_by_experience.value
    else:
        json_order_by_experience = order_by_experience
    params["order_by_experience"] = json_order_by_experience

    json_order_by_rating: Union[None, Unset, str]
    if isinstance(order_by_rating, Unset):
        json_order_by_rating = UNSET
    elif isinstance(order_by_rating, OrderByType):
        json_order_by_rating = order_by_rating.value
    else:
        json_order_by_rating = order_by_rating
    params["order_by_rating"] = json_order_by_rating

    json_is_deleted: Union[None, Unset, bool]
    if isinstance(is_deleted, Unset):
        json_is_deleted = UNSET
    else:
        json_is_deleted = is_deleted
    params["is_deleted"] = json_is_deleted

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/users/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, UserPaginationResponse]]:
    if response.status_code == 200:
        response_200 = UserPaginationResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, UserPaginationResponse]]:
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
    name_ilike: Union[None, Unset, str] = UNSET,
    order_by_gold: Union[None, OrderByType, Unset] = UNSET,
    order_by_experience: Union[None, OrderByType, Unset] = UNSET,
    order_by_rating: Union[None, OrderByType, Unset] = UNSET,
    is_deleted: Union[None, Unset, bool] = UNSET,
) -> Response[Union[HTTPValidationError, UserPaginationResponse]]:
    """Get Users

     Get a paginated list of users.

    Args:
        limit (Union[Unset, int]): Limit of items per page Default: 10.
        page (Union[Unset, int]): Page number Default: 1.
        ids (Union[None, Unset, list[UUID]]): User IDs to filter users by
        name_ilike (Union[None, Unset, str]): User name
        order_by_gold (Union[None, OrderByType, Unset]): Order by filter.
        order_by_experience (Union[None, OrderByType, Unset]): Order by filter.
        order_by_rating (Union[None, OrderByType, Unset]): Order by filter.
        is_deleted (Union[None, Unset, bool]): Object deleted inclusion filter.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UserPaginationResponse]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        page=page,
        ids=ids,
        name_ilike=name_ilike,
        order_by_gold=order_by_gold,
        order_by_experience=order_by_experience,
        order_by_rating=order_by_rating,
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
    name_ilike: Union[None, Unset, str] = UNSET,
    order_by_gold: Union[None, OrderByType, Unset] = UNSET,
    order_by_experience: Union[None, OrderByType, Unset] = UNSET,
    order_by_rating: Union[None, OrderByType, Unset] = UNSET,
    is_deleted: Union[None, Unset, bool] = UNSET,
) -> Optional[Union[HTTPValidationError, UserPaginationResponse]]:
    """Get Users

     Get a paginated list of users.

    Args:
        limit (Union[Unset, int]): Limit of items per page Default: 10.
        page (Union[Unset, int]): Page number Default: 1.
        ids (Union[None, Unset, list[UUID]]): User IDs to filter users by
        name_ilike (Union[None, Unset, str]): User name
        order_by_gold (Union[None, OrderByType, Unset]): Order by filter.
        order_by_experience (Union[None, OrderByType, Unset]): Order by filter.
        order_by_rating (Union[None, OrderByType, Unset]): Order by filter.
        is_deleted (Union[None, Unset, bool]): Object deleted inclusion filter.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UserPaginationResponse]
    """

    return sync_detailed(
        client=client,
        limit=limit,
        page=page,
        ids=ids,
        name_ilike=name_ilike,
        order_by_gold=order_by_gold,
        order_by_experience=order_by_experience,
        order_by_rating=order_by_rating,
        is_deleted=is_deleted,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 10,
    page: Union[Unset, int] = 1,
    ids: Union[None, Unset, list[UUID]] = UNSET,
    name_ilike: Union[None, Unset, str] = UNSET,
    order_by_gold: Union[None, OrderByType, Unset] = UNSET,
    order_by_experience: Union[None, OrderByType, Unset] = UNSET,
    order_by_rating: Union[None, OrderByType, Unset] = UNSET,
    is_deleted: Union[None, Unset, bool] = UNSET,
) -> Response[Union[HTTPValidationError, UserPaginationResponse]]:
    """Get Users

     Get a paginated list of users.

    Args:
        limit (Union[Unset, int]): Limit of items per page Default: 10.
        page (Union[Unset, int]): Page number Default: 1.
        ids (Union[None, Unset, list[UUID]]): User IDs to filter users by
        name_ilike (Union[None, Unset, str]): User name
        order_by_gold (Union[None, OrderByType, Unset]): Order by filter.
        order_by_experience (Union[None, OrderByType, Unset]): Order by filter.
        order_by_rating (Union[None, OrderByType, Unset]): Order by filter.
        is_deleted (Union[None, Unset, bool]): Object deleted inclusion filter.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UserPaginationResponse]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        page=page,
        ids=ids,
        name_ilike=name_ilike,
        order_by_gold=order_by_gold,
        order_by_experience=order_by_experience,
        order_by_rating=order_by_rating,
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
    name_ilike: Union[None, Unset, str] = UNSET,
    order_by_gold: Union[None, OrderByType, Unset] = UNSET,
    order_by_experience: Union[None, OrderByType, Unset] = UNSET,
    order_by_rating: Union[None, OrderByType, Unset] = UNSET,
    is_deleted: Union[None, Unset, bool] = UNSET,
) -> Optional[Union[HTTPValidationError, UserPaginationResponse]]:
    """Get Users

     Get a paginated list of users.

    Args:
        limit (Union[Unset, int]): Limit of items per page Default: 10.
        page (Union[Unset, int]): Page number Default: 1.
        ids (Union[None, Unset, list[UUID]]): User IDs to filter users by
        name_ilike (Union[None, Unset, str]): User name
        order_by_gold (Union[None, OrderByType, Unset]): Order by filter.
        order_by_experience (Union[None, OrderByType, Unset]): Order by filter.
        order_by_rating (Union[None, OrderByType, Unset]): Order by filter.
        is_deleted (Union[None, Unset, bool]): Object deleted inclusion filter.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UserPaginationResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            page=page,
            ids=ids,
            name_ilike=name_ilike,
            order_by_gold=order_by_gold,
            order_by_experience=order_by_experience,
            order_by_rating=order_by_rating,
            is_deleted=is_deleted,
        )
    ).parsed
