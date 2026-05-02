"""Normalize raw Socrata building footprint rows into Building objects."""
from __future__ import annotations

from nyczone.geo.transform import ring_to_local_meters
from nyczone.models.building import Building

_ZONING_PALETTE: dict[str, str] = {
    "R": "#F5DEB3",
    "C": "#4A90D9",
    "M": "#C0392B",
    "PARK": "#27AE60",
    "PA": "#27AE60",
    "BPC": "#8E44AD",
}
_DEFAULT_COLOR = "#95A5A6"


def _color_for(zoning: str) -> str:
    for prefix, color in _ZONING_PALETTE.items():
        if zoning.upper().startswith(prefix):
            return color
    return _DEFAULT_COLOR


def _category_for(zoning: str) -> str:
    for prefix in _ZONING_PALETTE:
        if zoning.upper().startswith(prefix):
            return prefix
    return "OTHER"


def _parse_rings(
    geom: dict, anchor_lon: float, anchor_lat: float  # type: ignore[type-arg]
) -> list[list[tuple[float, float]]]:
    geo_type = geom.get("type", "")
    if geo_type == "Polygon":
        raw_rings = geom["coordinates"]
    elif geo_type == "MultiPolygon":
        raw_rings = max(geom["coordinates"], key=len)
    else:
        return []
    return [ring_to_local_meters(ring, anchor_lon, anchor_lat) for ring in raw_rings]


def normalize_footprint(
    row: dict,  # type: ignore[type-arg]
    anchor_lon: float,
    anchor_lat: float,
    zoning_district: str = "",
) -> Building | None:
    geom = row.get("the_geom")
    if not geom:
        return None
    rings = _parse_rings(geom, anchor_lon, anchor_lat)
    if not rings or len(rings[0]) < 3:
        return None

    height_ft = float(row.get("heightroof") or 0)
    numfloors = int(float(row.get("numfloors") or 1))
    if height_ft <= 0:
        height_ft = numfloors * 11.48
        height_source = "numfloors"
    else:
        height_source = "heightroof"

    return Building(
        bin=str(row.get("bin", "")),
        numfloors=numfloors,
        height_ft=height_ft,
        height_source=height_source,
        rings=rings,
        zoning_district=zoning_district,
        zoning_category=_category_for(zoning_district),
        color_hex=_color_for(zoning_district),
    )
