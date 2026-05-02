"""Bounding box helpers (WGS84)."""
from dataclasses import dataclass


@dataclass(frozen=True)
class BBox:
    min_lon: float
    min_lat: float
    max_lon: float
    max_lat: float

    @classmethod
    def from_str(cls, s: str) -> "BBox":
        parts = [float(x) for x in s.split(",")]
        if len(parts) != 4:
            raise ValueError("bbox must be 'min_lon,min_lat,max_lon,max_lat'")
        return cls(*parts)

    @property
    def center(self) -> tuple[float, float]:
        return ((self.min_lon + self.max_lon) / 2, (self.min_lat + self.max_lat) / 2)

    def to_socrata_where(self, geom_col: str = "the_geom") -> str:
        return (
            f"within_box({geom_col}, {self.min_lat}, {self.min_lon}, "
            f"{self.max_lat}, {self.max_lon})"
        )

    def area_deg2(self) -> float:
        return (self.max_lon - self.min_lon) * (self.max_lat - self.min_lat)
