"""Coordinate transform: WGS84 ↔ NY State Plane (EPSG:2263) → local meters."""
from pyproj import Transformer

# US survey foot to meter
_FT_TO_M = 0.3048006096

_wgs84_to_2263 = Transformer.from_crs("EPSG:4326", "EPSG:2263", always_xy=True)
_2263_to_wgs84 = Transformer.from_crs("EPSG:2263", "EPSG:4326", always_xy=True)


def wgs84_to_state_plane(lon: float, lat: float) -> tuple[float, float]:
    """Returns (easting_ft, northing_ft) in EPSG:2263."""
    return _wgs84_to_2263.transform(lon, lat)


def state_plane_to_wgs84(easting_ft: float, northing_ft: float) -> tuple[float, float]:
    """Returns (lon, lat) in WGS84."""
    return _2263_to_wgs84.transform(easting_ft, northing_ft)


def to_local_meters(
    lon: float, lat: float, anchor_lon: float, anchor_lat: float
) -> tuple[float, float]:
    """Convert a WGS84 point to anchor-relative meters."""
    ax, ay = wgs84_to_state_plane(anchor_lon, anchor_lat)
    px, py = wgs84_to_state_plane(lon, lat)
    return (px - ax) * _FT_TO_M, (py - ay) * _FT_TO_M


def ring_to_local_meters(
    ring: list[list[float]], anchor_lon: float, anchor_lat: float
) -> list[tuple[float, float]]:
    """Convert a GeoJSON ring [[lon,lat],...] to local-meter tuples."""
    return [to_local_meters(pt[0], pt[1], anchor_lon, anchor_lat) for pt in ring]
