"""Export Building list as GeoJSON FeatureCollection (local-meter coordinates)."""
import json
from pathlib import Path

from nyczone.models.building import Building


def buildings_to_geojson(
    buildings: list[Building], anchor_lon: float, anchor_lat: float
) -> dict:
    features = []
    for b in buildings:
        features.append(
            {
                "type": "Feature",
                "geometry": None,  # geometry encoded in properties for SketchUp
                "properties": {
                    "bbl": b.bbl,
                    "bin": b.bin,
                    "address": b.address,
                    "zoning_district": b.zoning_district,
                    "zoning_category": b.zoning_category,
                    "height_ft": b.height_ft,
                    "height_m": round(b.height_m, 3),
                    "height_source": b.height_source,
                    "numfloors": b.numfloors,
                    "year_built": b.year_built,
                    "land_use": b.land_use,
                    "color_hex": b.color_hex,
                    "rings": b.rings,
                    "anchor_lon": anchor_lon,
                    "anchor_lat": anchor_lat,
                },
            }
        )
    return {"type": "FeatureCollection", "features": features}


def write_geojson(
    buildings: list[Building], anchor_lon: float, anchor_lat: float, path: Path
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = buildings_to_geojson(buildings, anchor_lon, anchor_lat)
    path.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
