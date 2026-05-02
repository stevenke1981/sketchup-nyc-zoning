"""Spatial join: tag building footprints with their zoning district."""
from __future__ import annotations

from shapely.geometry import MultiPolygon, Point, Polygon, shape
from shapely.strtree import STRtree

from nyczone.models.building import Building
from nyczone.models.zoning import ZoningDistrict


def _to_shapely(geom: dict) -> Polygon | MultiPolygon | None:  # type: ignore[type-arg]
    try:
        return shape(geom)
    except Exception:
        return None


def build_zoning_tree(
    districts: list[ZoningDistrict],
) -> tuple[STRtree, list[ZoningDistrict]]:
    """Build an STRtree over zoning district polygons for fast lookup."""
    valid: list[ZoningDistrict] = []
    geoms = []
    for d in districts:
        s = _to_shapely(d.geometry)
        if s and not s.is_empty:
            geoms.append(s)
            valid.append(d)
    return STRtree(geoms), valid


def _centroid_wgs84(
    rings: list[list[tuple[float, float]]], anchor_lon: float, anchor_lat: float
) -> tuple[float, float] | None:
    """Approximate centroid in WGS84 from anchor-relative-meter rings.

    Inverse of ring_to_local_meters: meters → EPSG:2263 feet → WGS84.
    For the purposes of point-in-polygon the approximation is sufficient.
    """
    from nyczone.geo.transform import state_plane_to_wgs84, wgs84_to_state_plane

    _FT_TO_M = 0.3048006096
    outer = rings[0]
    if not outer:
        return None
    ax, ay = wgs84_to_state_plane(anchor_lon, anchor_lat)
    xs = [ax + pt[0] / _FT_TO_M for pt in outer]
    ys = [ay + pt[1] / _FT_TO_M for pt in outer]
    cx_ft = sum(xs) / len(xs)
    cy_ft = sum(ys) / len(ys)
    lon, lat = state_plane_to_wgs84(cx_ft, cy_ft)
    return lon, lat


def tag_buildings_with_zoning(
    buildings: list[Building],
    districts: list[ZoningDistrict],
    anchor_lon: float,
    anchor_lat: float,
) -> list[Building]:
    """Return buildings with zoning_district / zoning_category / color_hex filled in."""
    if not districts:
        return buildings

    tree, valid_districts = build_zoning_tree(districts)
    district_geoms = [shape(d.geometry) for d in valid_districts]

    from nyczone.normalize.footprints import _category_for, _color_for

    tagged: list[Building] = []
    for b in buildings:
        centroid = _centroid_wgs84(b.rings, anchor_lon, anchor_lat)
        if centroid is None:
            tagged.append(b)
            continue

        pt = Point(centroid[0], centroid[1])
        candidate_idxs = tree.query(pt)
        zoning = ""
        for idx in candidate_idxs:
            if district_geoms[idx].contains(pt):
                zoning = valid_districts[idx].zoning_district
                break

        tagged.append(
            b.model_copy(
                update={
                    "zoning_district": zoning,
                    "zoning_category": _category_for(zoning),
                    "color_hex": _color_for(zoning),
                }
            )
        )
    return tagged
