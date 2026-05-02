"""Orchestrate fetch → normalize → transform → spatial join → return buildings."""
from nyczone.geo.bbox import BBox
from nyczone.geo.transform import ring_to_local_meters
from nyczone.models.building import Building
from nyczone.sources.socrata import fetch_dataset

ZONING_PALETTE: dict[str, str] = {
    "R": "#F5DEB3",
    "C": "#4A90D9",
    "M": "#C0392B",
    "PARK": "#27AE60",
    "PA": "#27AE60",
    "BPC": "#8E44AD",
}


def _category_and_color(zoning: str) -> tuple[str, str]:
    for prefix, color in ZONING_PALETTE.items():
        if zoning.upper().startswith(prefix):
            return prefix, color
    return "OTHER", "#95A5A6"


def _parse_geojson_rings(
    geom: dict, anchor_lon: float, anchor_lat: float
) -> list[list[tuple[float, float]]]:
    geo_type = geom.get("type", "")
    if geo_type == "Polygon":
        coords = geom["coordinates"]
    elif geo_type == "MultiPolygon":
        coords = geom["coordinates"][0]  # largest polygon only for now
    else:
        return []
    return [ring_to_local_meters(ring, anchor_lon, anchor_lat) for ring in coords]


async def fetch_buildings(
    bbox: BBox, anchor_lon: float, anchor_lat: float
) -> list[Building]:
    buildings: list[Building] = []
    async for page in fetch_dataset("footprints", bbox):
        for row in page:
            geom = row.get("the_geom")
            if not geom:
                continue
            rings = _parse_geojson_rings(geom, anchor_lon, anchor_lat)
            if not rings:
                continue

            height_ft = float(row.get("heightroof") or 0)
            numfloors = int(float(row.get("numfloors") or 1))
            if height_ft <= 0:
                height_ft = numfloors * 11.48  # ~3.5m per floor in feet
                height_source = "numfloors"
            else:
                height_source = "heightroof"

            buildings.append(
                Building(
                    bin=str(row.get("bin", "")),
                    numfloors=numfloors,
                    height_ft=height_ft,
                    height_source=height_source,
                    rings=rings,
                )
            )
    return buildings
