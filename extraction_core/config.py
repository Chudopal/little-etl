from ipaddress import IPv4Address
from pathlib import Path
from typing import TypeVar

import yaml
from pydantic import BaseModel, HttpUrl


class StarwarsService(BaseModel):
    """Class for representing
    external starwars service in the subsystem."""

    base: HttpUrl | IPv4Address
    characters: str
    planets: str
    records_per_page: int
    page_literal: str

class FileStorage(BaseModel):
    """Represents basic path to user's files."""

    path: Path
    planets: Path
    characters: Path
    fetches_path: Path

class Config(BaseModel):
    """Class for representing all config
    for the the subsystem."""

    starwars_service: StarwarsService | None
    file_storage: FileStorage | None


TC = TypeVar('TC', bound=Config)


def init_config(config_path: str, config_model: type[TC]) -> TC:
    """Loads config from passed path."""
    config_raw = yaml.safe_load(Path(config_path).read_text())
    return config_model(**config_raw)
