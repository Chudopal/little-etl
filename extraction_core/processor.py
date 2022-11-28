from datetime import date

from pydantic import AnyUrl, BaseModel

from extraction_core.source_models import CanBeUnknown, Character, World


class ExtractedCharacterModel(BaseModel):
    """Common model for representation the character."""

    name: str
    date: date
    height: CanBeUnknown[int]
    mass: CanBeUnknown[int]
    hair_color: CanBeUnknown[str]
    skin_color: CanBeUnknown[str]
    eye_color: CanBeUnknown[str]
    birth_year: CanBeUnknown[str]
    gender: CanBeUnknown[str]
    homeworld: CanBeUnknown[str]


class GroupingResult(BaseModel):
    """Common model for representation
    result of characters' grouping.
    """

    name: str | None
    date: date | None
    height: CanBeUnknown[int | None]
    mass: CanBeUnknown[int | None]
    hair_color: CanBeUnknown[str | None]
    skin_color: CanBeUnknown[str | None]
    eye_color: CanBeUnknown[str | None]
    birth_year: CanBeUnknown[str | None]
    gender: CanBeUnknown[str | None]
    homeworld: CanBeUnknown[str | None]
    count: int | None


def _extract_homeworld_name(
    homeworld_link: str,
    worlds_source: CanBeUnknown[AnyUrl],
) -> World | None:
    return next(iter(filter(
        lambda world: world.url == homeworld_link,
        worlds_source
    )), None)


def _create_extracted_model(
    character_source: Character,
    worlds_source: tuple[World, ...],
) -> ExtractedCharacterModel:
    homeworld = _extract_homeworld_name(character_source.homeworld, worlds_source)
    return ExtractedCharacterModel(
        name=character_source.name,
        height=character_source.height,
        mass=character_source.mass,
        hair_color=character_source.hair_color,
        skin_color=character_source.skin_color,
        eye_color=character_source.eye_color,
        birth_year=character_source.birth_year,
        gender=character_source.gender,
        homeworld=homeworld.name if homeworld else 'unknown',
        date=character_source.edited,
    )


def extract(
    characters_results: tuple[Character, ...],
    worlds_results: tuple[World, ...],
) -> tuple[ExtractedCharacterModel, ...]:
    """Creates the representational model of character
    based on sequence of characters and worlds.
    """
    return tuple(
        _create_extracted_model(character_source, worlds_results)
        for character_source in characters_results
    )
