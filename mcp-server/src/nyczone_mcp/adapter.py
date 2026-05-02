"""Thin adapter: converts MCP tool requests into nyczone pipeline calls."""
from __future__ import annotations

from typing import Any

from nyczone.export.geojson import buildings_to_geojson
from nyczone.geo.bbox import BBox
from nyczone.pipeline import fetch_buildings


async def buildings_for_bbox(
    min_lon: float, min_lat: float, max_lon: float, max_lat: float, limit: int = 500
) -> dict[str, Any]:
    bbox = BBox(min_lon, min_lat, max_lon, max_lat)
    anchor_lon, anchor_lat = bbox.center
    buildings = await fetch_buildings(bbox, anchor_lon, anchor_lat)
    buildings = buildings[:limit]
    return buildings_to_geojson(buildings, anchor_lon, anchor_lat)
