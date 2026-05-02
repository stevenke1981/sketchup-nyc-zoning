from __future__ import annotations

import json
from pathlib import Path

import pytest
from conftest import ANCHOR_LAT, ANCHOR_LON, SAMPLE_FOOTPRINT_ROW
from nyczone.export.geojson import buildings_to_geojson, write_geojson
from nyczone.normalize.footprints import normalize_footprint


@pytest.fixture()
def building():
    return normalize_footprint(SAMPLE_FOOTPRINT_ROW, ANCHOR_LON, ANCHOR_LAT, "C5-3")


def test_geojson_structure(building):
    fc = buildings_to_geojson([building], ANCHOR_LON, ANCHOR_LAT)
    assert fc["type"] == "FeatureCollection"
    assert len(fc["features"]) == 1
    feat = fc["features"][0]
    props = feat["properties"]
    assert "rings" in props
    assert "height_m" in props
    assert "color_hex" in props
    assert props["color_hex"] == "#4A90D9"


def test_geojson_anchor(building):
    fc = buildings_to_geojson([building], ANCHOR_LON, ANCHOR_LAT)
    props = fc["features"][0]["properties"]
    assert props["anchor_lon"] == pytest.approx(ANCHOR_LON)
    assert props["anchor_lat"] == pytest.approx(ANCHOR_LAT)


def test_write_geojson(building, tmp_path):
    out = tmp_path / "test.geojson"
    write_geojson([building], ANCHOR_LON, ANCHOR_LAT, out)
    assert out.exists()
    data = json.loads(out.read_text())
    assert data["type"] == "FeatureCollection"


def test_empty_list():
    fc = buildings_to_geojson([], ANCHOR_LON, ANCHOR_LAT)
    assert fc["features"] == []
