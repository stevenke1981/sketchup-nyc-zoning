"""Tool: get_borough_stats — summary stats for a borough."""
from typing import Any

import httpx

from nyczone.config import settings
from nyczone.geo.borough_bboxes import BOROUGH_BBOXES

FOOTPRINTS_URL = "https://data.cityofnewyork.us/resource/qrmh-6wdr.json"


async def get_borough_stats(borough: str) -> dict[str, Any]:
    """Return building count and average height for a borough."""
    borough = borough.lower()
    if borough not in BOROUGH_BBOXES:
        return {"error": f"Unknown borough '{borough}'. Options: {list(BOROUGH_BBOXES)}"}

    bbox = BOROUGH_BBOXES[borough]
    headers = {}
    if settings.app_token:
        headers["X-App-Token"] = settings.app_token

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            FOOTPRINTS_URL,
            params={
                "$select": "count(*) AS total, avg(heightroof) AS avg_height_ft",
                "$where": bbox.to_socrata_where(),
            },
            headers=headers,
            timeout=20.0,
        )
        resp.raise_for_status()
        rows = resp.json()

    if not rows:
        return {"borough": borough, "total": 0, "avg_height_ft": 0}

    row = rows[0]
    return {
        "borough": borough,
        "total_buildings": int(row.get("total", 0)),
        "avg_height_ft": round(float(row.get("avg_height_ft") or 0), 1),
    }
