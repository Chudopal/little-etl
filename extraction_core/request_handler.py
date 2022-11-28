from functools import reduce
from urllib.parse import urljoin

from pydantic import AnyUrl

from extraction_core.config import StarwarsService
from extraction_core.source_models import Character, World


def calculate_worlds_links(
    starwars_service_config: StarwarsService,
    characters: tuple[Character, ...],
    saved_worlds: tuple[World, ...]
) -> set[AnyUrl]:
    """Optimize the number of external
    requests for receiving the worlds.
    """
    saved_worlds_ids = {world.id for world in saved_worlds}
    return {
        _calculate_page(
            starwars_service_config,
            character_source.homeworld_id,
        )
        for character_source in characters
        if character_source.homeworld_id not in saved_worlds_ids
    }


def calculate_characters_links(
    starwars_service_config: StarwarsService,
    characters: tuple[Character, ...],
    max_page: int,
) -> set[AnyUrl]:
    """Optimize the number of external
    requests for receiving the characters.
    """
    return {
        _page_request_builder(
            starwars_service_config,
            starwars_service_config.characters,
            page,
        )
        for page in range(max_page, 0, -1)
        if not _is_already_fetched(
            starwars_service_config,
            page,
            characters,
        )
    }


def _calculate_page(
    starwars_service_config: StarwarsService,
    homeworld_id: AnyUrl,
    ) -> int:
    page_number = (homeworld_id
        // starwars_service_config.records_per_page
        + 1
    )
    return _page_request_builder(
        starwars_service_config,
        starwars_service_config.planets,
        page_number,
    )


def _page_request_builder(
    starwars_service_config: StarwarsService,
    endpoint: str,
    page: str
) -> AnyUrl:
    url_tamplate = reduce(urljoin, [
        starwars_service_config.base,
        endpoint,
        f'?{starwars_service_config.page_literal}',
    ]) + '={}'
    return url_tamplate.format(page)


def _is_already_fetched(
    starwars_service_config: StarwarsService,
    page: int,
    entities: tuple[World | Character, ...],
) -> bool:
    max_id = page * starwars_service_config.records_per_page
    return max_id in {entity.id for entity in entities}
