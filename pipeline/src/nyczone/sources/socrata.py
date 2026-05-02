"""Async Socrata client with retry, pagination, and bbox filtering."""
from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from nyczone.config import settings
from nyczone.geo.bbox import BBox

SOCRATA_BASE = "https://data.cityofnewyork.us/resource"

DATASET_IDS = {
    "footprints": "qrmh-6wdr",
    "pluto": "64uk-42ks",
    "zoning": "6tn7-vhp3",
}


def _headers() -> dict[str, str]:
    h = {"Accept": "application/json"}
    if settings.app_token:
        h["X-App-Token"] = settings.app_token
    return h


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=30))
async def _get(client: httpx.AsyncClient, url: str, params: dict[str, Any]) -> list[dict]:
    resp = await client.get(url, params=params, headers=_headers(), timeout=30.0)
    resp.raise_for_status()
    return resp.json()


async def fetch_dataset(
    dataset: str, bbox: BBox, extra_where: str = ""
) -> AsyncIterator[list[dict]]:
    """Yield pages of records for a dataset within bbox."""
    dataset_id = DATASET_IDS[dataset]
    url = f"{SOCRATA_BASE}/{dataset_id}.json"
    where = bbox.to_socrata_where()
    if extra_where:
        where = f"{where} AND {extra_where}"

    async with httpx.AsyncClient() as client:
        offset = 0
        fetched = 0
        while True:
            params = {
                "$where": where,
                "$limit": settings.socrata_limit,
                "$offset": offset,
            }
            rows = await _get(client, url, params)
            if not rows:
                break
            yield rows
            fetched += len(rows)
            if fetched >= settings.max_features:
                break
            if len(rows) < settings.socrata_limit:
                break
            offset += settings.socrata_limit
