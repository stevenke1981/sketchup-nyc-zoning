"""Tool: query_buildings — returns GeoJSON FeatureCollection for a bbox."""
import asyncio
from typing import Any

from nyczone.export.geojson import buildings_to_geojson
from nyczone.geo.bbox import BBox
from nyczone.pipeline import fetch_buildings


async def query_buildings(
    min_lon: float,
    min_lat: float,
    max_lon: float,
    max_lat: float,
    limit: int = 500,
) -> dict[str, Any]:
    """
    Return buildings within the bounding box as a GeoJSON FeatureCollection.
    Coordinates in each feature's `rings` property are anchor-relative meters.
    """
    bbox = BBox(min_lon, min_lat, max_lon, max_lat)
    anchor_lon, anchor_lat = bbox.center
    buildings = await fetch_buildings(bbox, anchor_lon, anchor_lat)
    buildings = buildings[:limit]
    return buildings_to_geojson(buildings, anchor_lon, anchor_lat)
