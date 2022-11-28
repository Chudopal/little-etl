from extraction_core.request_handler import calculate_worlds_links
from extraction_core.source_models import StarwarsData, World
from tests.data.extracting_data import CHARACTER_DATA, WORLD_PAGES_URLS, SAVED_WORLDS


def test_calculate_worlds_links(config):
    links = calculate_worlds_links(
        config.starwars_service,
        StarwarsData(**CHARACTER_DATA).results,
        [World(**item) for item in SAVED_WORLDS],
    )
    assert links == WORLD_PAGES_URLS
