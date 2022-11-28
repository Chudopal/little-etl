from collections import Counter

from extraction_core.config import Config
from extraction_core.fetcher import make_external_requests
from extraction_core.processor import (
    ExtractedCharacterModel, GroupingResult, extract,
)
from extraction_core.request_handler import (
    calculate_characters_links, calculate_worlds_links,
)
from extraction_core.source_models import Character, World
from extraction_core.storage_handler import read, save_source_to_storage


async def retreive_new_collection(config: Config, page: int, params: list[str]) -> tuple[dict]:
    characters = await _handle_characters(config, page)
    worlds = await _handle_worlds(config, characters)
    return _group_characters(extract(characters, worlds), params)


def _group_characters(
    characters: tuple[ExtractedCharacterModel],
    params: tuple[str],
) -> tuple[ExtractedCharacterModel | GroupingResult, ...]:
    result = characters
    if params:
        counter = Counter([
            tuple(character.dict().get(param) for param in params)
            for character in characters
        ])
        result = tuple(
            GroupingResult(**dict(zip(params+('count',), field + (count,))))
            for field, count in counter.items()
        )
    return result


async def _handle_characters(config: Config, page) -> tuple[Character]:
    characters = read(
        config.file_storage,
        config.file_storage.characters,
    )

    character_links = calculate_characters_links(
        config.starwars_service,
        characters,
        page,
    )
    characters += await make_external_requests(character_links)

    save_source_to_storage(config.file_storage, characters)

    return tuple(filter(
        lambda character: character.id <= page * config.starwars_service.records_per_page,
        characters,
    ))


async def _handle_worlds(config: Config, characters: tuple[Character]) -> tuple[World]:
    worlds = read(
        config.file_storage,
        config.file_storage.planets,
    )

    worlds_links = calculate_worlds_links(
        config.starwars_service,
        characters,
        worlds,
    )
    worlds += await make_external_requests(worlds_links)

    save_source_to_storage(config.file_storage, worlds)

    return worlds
