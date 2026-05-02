"""Tool: search_by_address — geocode NYC address via NYC GeoSearch (free)."""
from typing import Any

import httpx

GEOSEARCH_URL = "https://geosearch.planninglabs.nyc/v2/search"


async def search_by_address(address: str) -> dict[str, Any]:
    """Geocode a NYC address and return coordinates + suggested bbox."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            GEOSEARCH_URL,
            params={"text": address, "size": 1},
            timeout=10.0,
        )
        resp.raise_for_status()
        data = resp.json()

    features = data.get("features", [])
    if not features:
        return {"error": f"Address not found: {address}"}

    feat = features[0]
    lon, lat = feat["geometry"]["coordinates"]
    props = feat.get("properties", {})
    delta = 0.002  # ~200m radius bbox
    return {
        "address": props.get("label", address),
        "lon": lon,
        "lat": lat,
        "bbl": props.get("pad_bbl", ""),
        "suggested_bbox": {
            "min_lon": lon - delta,
            "min_lat": lat - delta,
            "max_lon": lon + delta,
            "max_lat": lat + delta,
        },
    }
