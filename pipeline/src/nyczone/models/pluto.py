from __future__ import annotations

from pydantic import BaseModel, field_validator


class Pluto(BaseModel):
    bbl: str = ""
    address: str = ""
    zipcode: str = ""
    borough: str = ""
    year_built: int = 0
    numfloors: int = 1
    land_use: str = ""
    far: float = 0.0
    lot_area_sqft: float = 0.0
    bldg_area_sqft: float = 0.0

    @field_validator("year_built", "numfloors", mode="before")
    @classmethod
    def coerce_int(cls, v: object) -> int:
        try:
            return int(float(v))  # type: ignore[arg-type]
        except (TypeError, ValueError):
            return 0

    @field_validator("far", "lot_area_sqft", "bldg_area_sqft", mode="before")
    @classmethod
    def coerce_float(cls, v: object) -> float:
        try:
            return float(v)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            return 0.0
