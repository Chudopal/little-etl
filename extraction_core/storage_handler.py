import json
import os
from datetime import datetime
from hashlib import md5
from pathlib import Path
from typing import Sequence

import petl
from pydantic import BaseModel

from extraction_core.config import FileStorage
from extraction_core.processor import ExtractedCharacterModel
from extraction_core.source_models import Character, World


class StorageResponse(BaseModel):
    items: tuple[World | Character | ExtractedCharacterModel, ...]


def save_source_to_storage(
    file_storage_config: FileStorage,
    data_source: tuple[World | Character, ...],
) -> None:
    saving_path = None
    match data_source:
        case Character(), *_:
            saving_path = file_storage_config.path.joinpath(
                file_storage_config.characters,
            )
        case World(), *_:
            saving_path = file_storage_config.path.joinpath(
                file_storage_config.planets,
            )
    if saving_path:
        data_table_items = _serialise_to_table(data_source)
        _save(data_table_items, saving_path)


def read(file_storage_config: FileStorage, storage: Path) -> tuple[tuple]:
    return _deserialise_from_table(petl.fromcsv(
        file_storage_config.path.joinpath(
            storage,
        ),
    ).tuple())


def save_clear_data_to_storage(
    file_storage_config: FileStorage,
    data_items: Sequence[ExtractedCharacterModel],
) -> tuple[str, str]:
    filename = datetime.now().isoformat() + '.csv'

    path = file_storage_config.path.joinpath(
        file_storage_config.fetches_path.joinpath(
            Path(filename)
        )
    )

    table_data_items = _serialise_to_table(data_items)
    _save(table_data_items, path)
    return path, str(md5(filename.encode()).hexdigest()) + '.csv'


def get_all_fetches_names(
    file_storage_config: FileStorage,
):
    path = file_storage_config.path.joinpath(
        file_storage_config.fetches_path,
    )
    return tuple(
        filepath.name for filepath in os.scandir(path)
        if filepath.is_file()
    )


def _save(
    table_data_items: list[list],
    path: Path,
) -> None:
    csv_table = petl.wrap(table_data_items)
    petl.tocsv(csv_table, path)


def _serialise_to_table(source_items: tuple[World | Character, ...]) -> list[list]:
    return [
        source_items[0].dict(exclude_none=True).keys(),
        *(
            json.loads(data_item.json(exclude_none=True)).values()
            for data_item in source_items
        )
    ] if source_items else []


def _deserialise_from_table(
    raw_data: tuple[tuple],
) -> tuple[Character | World | ExtractedCharacterModel, ...]:
    entities = ()
    if raw_data:
        schema, *payload = raw_data
        entities = StorageResponse(
            items=[dict(zip(schema, data_item)) for data_item in payload]
        ).items
    return entities
