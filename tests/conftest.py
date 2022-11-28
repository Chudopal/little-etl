from pytest import fixture
from extraction_core.config import Config

@fixture
def config():
    return Config(**{
        "starwars_service":{
            "base": "https://swapi.dev/api/",
            "characters": "people/",
            "planets": "planets/",
            "records_per_page": 10,
            "page_literal": "page",
        },
        "file_storage": {
            "path": "./fetches_storage/",
            "fetches_path": "fetches/",
            "planets": "planets.csv",
            "characters": "characters.csv",
        }
    })