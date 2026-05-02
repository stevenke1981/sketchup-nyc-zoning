"""Orchestrate: fetch footprints + PLUTO → join by BBL → return Buildings.

Data sources (verified 2026-05):
  footprints: 5zhs-2jue  (the_geom polygon + height_roof + mappluto_bbl)
  pluto:      64uk-42ks  (zonedist1 + numfloors + yearbuilt + address, filtered by lat/lon)
"""
from __future__ import annotations

import asyncio

from nyczone.geo.bbox import BBox
from nyczone.models.building import Building
from nyczone.normalize.footprints import _category_for, _color_for, normalize_footprint
from nyczone.normalize.pluto import normalize_pluto
from nyczone.sources.socrata import fetch_dataset, fetch_pluto_in_bbox


def _normalize_bbl(raw: object) -> str:
    """Normalize BBL to 10-digit string (handles '1007220039.00000000' → '1007220039')."""
    try:
        return str(int(float(str(raw))))  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return ""


async def _fetch_pluto_lookup(bbox: BBox) -> dict[str, dict]:  # type: ignore[type-arg]
    """Return {bbl_str: pluto_row} for the bbox."""
    lookup: dict[str, dict] = {}  # type: ignore[type-arg]
    async for page in fetch_pluto_in_bbox(bbox):
        for row in page:
            bbl = _normalize_bbl(row.get("bbl", ""))
            if bbl:
                lookup[bbl] = row
    return lookup


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


async def fetch_buildings(
    bbox: BBox, anchor_lon: float, anchor_lat: float
) -> list[Building]:
    """Fetch buildings with footprint geometry and zoning from PLUTO."""
    footprint_task = asyncio.create_task(_fetch_raw_footprints(bbox, anchor_lon, anchor_lat))
    pluto_task = asyncio.create_task(_fetch_pluto_lookup(bbox))

    buildings, pluto_lookup = await asyncio.gather(footprint_task, pluto_task)

    # Join footprints → PLUTO by BBL to get zoning + metadata
    result: list[Building] = []
    for b in buildings:
        pluto = pluto_lookup.get(_normalize_bbl(b.bbl), {})
        zoning = str(pluto.get("zonedist1", ""))
        result.append(
            b.model_copy(
                update={
                    "zoning_district": zoning,
                    "zoning_category": _category_for(zoning),
                    "color_hex": _color_for(zoning),
                    "address": str(pluto.get("address", "")),
                    "year_built": int(float(pluto.get("yearbuilt") or 0)),
                    "numfloors": int(float(pluto.get("numfloors") or b.numfloors)),
                    "land_use": str(pluto.get("landuse", "")),
                }
            )
        )
    return result
