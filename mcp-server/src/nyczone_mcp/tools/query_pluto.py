"""Tool: query_pluto — lookup by BBL."""
from typing import Any

import httpx

from nyczone.config import settings

PLUTO_URL = "https://data.cityofnewyork.us/resource/64uk-42ks.json"


async def query_pluto(bbl: str) -> dict[str, Any]:
    """Return PLUTO data for a given BBL (10-digit Borough-Block-Lot)."""
    headers = {}
    if settings.app_token:
        headers["X-App-Token"] = settings.app_token
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            PLUTO_URL,
            params={"$where": f"bbl='{bbl}'", "$limit": 1},
            headers=headers,
            timeout=15.0,
        )
        resp.raise_for_status()
        rows = resp.json()
    if not rows:
        return {"error": f"BBL {bbl} not found"}
    row = rows[0]
    return {
        "bbl": bbl,
        "address": row.get("address", ""),
        "zipcode": row.get("zipcode", ""),
        "borough": row.get("borough", ""),
        "year_built": row.get("yearbuilt", ""),
        "numfloors": row.get("numfloors", ""),
        "land_use": row.get("landuse", ""),
        "far": row.get("builtfar", ""),
        "lot_area_sqft": row.get("lotarea", ""),
        "bldg_area_sqft": row.get("bldgarea", ""),
    }
