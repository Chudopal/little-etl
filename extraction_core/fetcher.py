import asyncio
from typing import Sequence

from aiohttp import ClientSession

from extraction_core.source_models import Character, StarwarsData, World


async def fetch_data(url, session) -> tuple[dict, int]:
    async with session.get(url, ssl=False) as response:
        return await response.json()


def wrap_into_model(model_raw_data) -> tuple[World | Character, ...]:
    """Raw data -> internal model."""
    return StarwarsData(
        **{
            **model_raw_data[-1],  # TODO: handle case if 404
            'results': sum(
                [payload.get('results') for payload in model_raw_data],
                start=[],
            )
        }
    ).results if model_raw_data else ()


async def make_external_requests(urls: Sequence[str]) -> tuple[World | Character, ...]:
    """Execute asynchronous bunch of requests to external services."""
    async with ClientSession() as session:  # TODO: it's better to create persistent session objects
        tasks = (
            asyncio.ensure_future(fetch_data(url, session))
            for url in urls
        )
        responses = await asyncio.gather(*tasks)
    return wrap_into_model(responses)
