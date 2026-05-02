"""Normalize raw MapPLUTO rows into Pluto objects."""
from __future__ import annotations

from nyczone.models.pluto import Pluto


def normalize_pluto(row: dict) -> Pluto:  # type: ignore[type-arg]
    return Pluto(
        bbl=str(row.get("bbl", "")),
        address=str(row.get("address", "")),
        zipcode=str(row.get("zipcode", "")),
        borough=str(row.get("borough", "")),
        year_built=row.get("yearbuilt", 0),
        numfloors=row.get("numfloors", 1),
        land_use=str(row.get("landuse", "")),
        far=row.get("builtfar", 0.0),
        lot_area_sqft=row.get("lotarea", 0.0),
        bldg_area_sqft=row.get("bldgarea", 0.0),
    )
