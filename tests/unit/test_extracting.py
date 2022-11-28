from extraction_core.processor import ExtractedCharacterModel, extract
from extraction_core.source_models import StarwarsData
from tests.data.extracting_data import (
    CHARACTER_DATA,
    EXTRACTED_DATA,
    WORLDS_DATA,
)


def test_extract():
    characters = StarwarsData(**CHARACTER_DATA).results
    worlds = StarwarsData(**WORLDS_DATA).results
    result = tuple(
        ExtractedCharacterModel(**extracted_charater_data)
        for extracted_charater_data in EXTRACTED_DATA
    )
    assert result == extract(characters, worlds)
