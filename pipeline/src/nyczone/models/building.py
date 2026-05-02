from pydantic import BaseModel, Field, field_validator


class Building(BaseModel):
    bin: str = ""
    bbl: str = ""
    address: str = ""
    zipcode: str = ""
    borough: str = ""
    height_ft: float = 3.28  # ~1m floor placeholder
    numfloors: int = 1
    year_built: int = 0
    land_use: str = ""
    zoning_district: str = ""
    zoning_category: str = ""
    height_source: str = "placeholder"
    # Local-meter rings: outer ring first, then holes
    rings: list[list[tuple[float, float]]] = Field(default_factory=list)
    color_hex: str = "#95A5A6"

    @field_validator("height_ft", mode="before")
    @classmethod
    def coerce_height(cls, v: object) -> float:
        try:
            f = float(v)  # type: ignore[arg-type]
            return f if f > 0 else 3.28
        except (TypeError, ValueError):
            return 3.28

    @property
    def height_m(self) -> float:
        return self.height_ft * 0.3048
