"""CLI: nyczone fetch | build-cache | export."""
import asyncio
from pathlib import Path

import typer

from nyczone.geo.bbox import BBox

app = typer.Typer(help="NYC Zoning data pipeline")


@app.command()
def fetch(
    bbox: str = typer.Option(..., help="min_lon,min_lat,max_lon,max_lat"),
    out: Path = typer.Option(..., help="Output GeoJSON path"),
) -> None:
    """Fetch buildings for a bounding box and write GeoJSON."""
    from nyczone.export.geojson import write_geojson
    from nyczone.pipeline import fetch_buildings

    box = BBox.from_str(bbox)
    anchor_lon, anchor_lat = box.center
    typer.echo(f"Fetching bbox={bbox} anchor=({anchor_lon:.4f},{anchor_lat:.4f})")
    buildings = asyncio.run(fetch_buildings(box, anchor_lon, anchor_lat))
    write_geojson(buildings, anchor_lon, anchor_lat, out)
    typer.echo(f"Wrote {len(buildings)} buildings → {out}")


@app.command()
def build_cache(
    borough: str = typer.Option(..., help="manhattan|brooklyn|queens|bronx|statenisland"),
) -> None:
    """Fetch and cache an entire borough (slow, ~5 min)."""
    from nyczone.geo.borough_bboxes import BOROUGH_BBOXES
    from nyczone.pipeline import fetch_buildings

    if borough not in BOROUGH_BBOXES:
        typer.echo(f"Unknown borough: {borough}. Options: {list(BOROUGH_BBOXES)}")
        raise typer.Exit(1)
    box = BOROUGH_BBOXES[borough]
    anchor_lon, anchor_lat = box.center
    typer.echo(f"Building cache for {borough}...")
    buildings = asyncio.run(fetch_buildings(box, anchor_lon, anchor_lat))
    typer.echo(f"Cached {len(buildings)} buildings for {borough}")


if __name__ == "__main__":
    app()
