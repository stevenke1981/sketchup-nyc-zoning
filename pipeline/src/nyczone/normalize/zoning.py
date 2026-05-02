"""Normalize raw zoning district rows into ZoningDistrict objects."""
from __future__ import annotations

from nyczone.models.zoning import ZoningDistrict


def normalize_zoning(row: dict) -> ZoningDistrict:  # type: ignore[type-arg]
    return ZoningDistrict(
        zoning_district=str(row.get("zonedist", "")),
        label=str(row.get("label", "")),
        geometry=row.get("the_geom", {}),
    )
