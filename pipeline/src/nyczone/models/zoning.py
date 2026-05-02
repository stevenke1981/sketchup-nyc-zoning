from __future__ import annotations

from pydantic import BaseModel


class ZoningDistrict(BaseModel):
    zoning_district: str = ""
    label: str = ""
    # Raw GeoJSON geometry (kept as-is for spatial join)
    geometry: dict = {}  # type: ignore[type-arg]
