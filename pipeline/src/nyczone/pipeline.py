"""Orchestrate: fetch → normalize → spatial join → return Buildings."""
from __future__ import annotations

import asyncio

from nyczone.geo.bbox import BBox
from nyczone.geo.spatial_join import tag_buildings_with_zoning
from nyczone.models.building import Building
from nyczone.models.zoning import ZoningDistrict
from nyczone.normalize.footprints import normalize_footprint
from nyczone.normalize.zoning import normalize_zoning
from nyczone.sources.socrata import fetch_dataset


async def _fetch_zoning(bbox: BBox) -> list[ZoningDistrict]:
    districts: list[ZoningDistrict] = []
    async for page in fetch_dataset("zoning", bbox):
        for row in page:
            if row.get("the_geom"):
                districts.append(normalize_zoning(row))
    return districts


async def fetch_buildings(
    bbox: BBox, anchor_lon: float, anchor_lat: float
) -> list[Building]:
    # Fetch footprints and zoning in parallel
    footprint_task = asyncio.create_task(_fetch_raw_footprints(bbox, anchor_lon, anchor_lat))
    zoning_task = asyncio.create_task(_fetch_zoning(bbox))

    buildings, districts = await asyncio.gather(footprint_task, zoning_task)

    if districts:
        buildings = tag_buildings_with_zoning(buildings, districts, anchor_lon, anchor_lat)

    return buildings


async def _fetch_raw_footprints(
    bbox: BBox, anchor_lon: float, anchor_lat: float
) -> list[Building]:
    buildings: list[Building] = []
    async for page in fetch_dataset("footprints", bbox):
        for row in page:
            b = normalize_footprint(row, anchor_lon, anchor_lat)
            if b:
                buildings.append(b)
    return buildings
