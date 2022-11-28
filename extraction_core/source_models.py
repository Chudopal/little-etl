import json
from datetime import datetime
from pathlib import PurePosixPath
from typing import Literal, Sequence, TypeVar

from pydantic import AnyUrl, BaseModel, validator

T = TypeVar('T')
CanBeUnknown = T | Literal['unknown'] | Literal['n/a']


def _normalize_collection(value: Sequence | str) -> tuple:
    if isinstance(value, str):
        value = json.loads(value.replace("'", '"'))
    return tuple(value)


def _extract_id(value: int, values: dict, url_label) -> int:
    if not value:
        value = int(
            PurePosixPath(values.get(url_label)).parts[-1],
        )
    return value


def _normalize_int(value):
    if isinstance(value, str):
        value = value.replace(',', '')
    return value


class _InnerBaseModel(BaseModel):
    name: str
    url: AnyUrl
    films: tuple[AnyUrl, ...]
    created: datetime
    edited: datetime
    id: int | None


class Character(_InnerBaseModel):
    """Represents the source data of character."""

    skin_color: str
    species: tuple[AnyUrl, ...]
    vehicles: tuple[AnyUrl, ...]
    starships: tuple[AnyUrl, ...]
    eye_color: CanBeUnknown[str]
    birth_year: CanBeUnknown[str]
    gender: CanBeUnknown[str]
    homeworld: CanBeUnknown[AnyUrl]
    hair_color: CanBeUnknown[str]
    height: CanBeUnknown[int | float]
    mass: CanBeUnknown[int | float]
    homeworld_id: int | None

    _normalize_int_fields = validator(
        'mass', 'height',
        pre=True, allow_reuse=True
    )(_normalize_int)

    _normalize_tuple = validator(
        'films', 'species', 'vehicles', 'starships',
        allow_reuse=True, pre=True,
    )(_normalize_collection)

    _normalize_id = validator(
        'id',
        pre=True, always=True, allow_reuse=True
    )(lambda value, values: _extract_id(value, values, 'url'))

    _normalize_homeworld_id = validator(
        'homeworld_id',
        pre=True, always=True, allow_reuse=True
    )(lambda value, values: _extract_id(value, values, 'homeworld'))


class World(_InnerBaseModel):
    """Represents the source data of world."""

    terrain: str
    surface_water: str
    residents: tuple[AnyUrl, ...]
    population: CanBeUnknown[int | float]
    rotation_period: CanBeUnknown[int | float]
    orbital_period: CanBeUnknown[int | float]
    diameter: CanBeUnknown[int | float]
    climate: CanBeUnknown[str]
    gravity: CanBeUnknown[str]

    _normalize_tuple = validator(
        'films', 'residents', allow_reuse=True, pre=True,
    )(_normalize_collection)

    _normalize_id = validator(
        'id',
        pre=True, always=True, allow_reuse=True
    )(lambda value, values: _extract_id(value, values, 'url'))

    _normalize_int_fields = validator(
        'population', 'rotation_period', 'orbital_period', 'diameter',
        pre=True, allow_reuse=True
    )(_normalize_int)



class StarwarsData(BaseModel):
    """Any request from source service."""

    count: int
    next: AnyUrl | None
    previous: AnyUrl | None
    results: tuple[Character | World, ...]
