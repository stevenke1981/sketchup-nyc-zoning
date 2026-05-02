"""Tool: query_zoning_district — point-in-polygon lookup."""
from typing import Any

from nyczone.geo.bbox import BBox
from nyczone.sources.socrata import fetch_dataset


async def query_zoning_district(lon: float, lat: float) -> dict[str, Any]:
    """Return the zoning district for a lat/lon point."""
    delta = 0.001
    bbox = BBox(lon - delta, lat - delta, lon + delta, lat + delta)
    async for page in fetch_dataset("zoning", bbox):
        for row in page:
            return {
                "zoning_district": row.get("zonedist", ""),
                "label": row.get("label", ""),
                "lon": lon,
                "lat": lat,
            }
    return {"zoning_district": None, "label": None, "lon": lon, "lat": lat}
