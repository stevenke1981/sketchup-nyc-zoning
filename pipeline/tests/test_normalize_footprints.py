from __future__ import annotations

import pytest
from conftest import ANCHOR_LAT, ANCHOR_LON, SAMPLE_FOOTPRINT_ROW
from nyczone.normalize.footprints import normalize_footprint


def test_normalize_basic():
    b = normalize_footprint(SAMPLE_FOOTPRINT_ROW, ANCHOR_LON, ANCHOR_LAT)
    assert b is not None
    assert b.height_ft == pytest.approx(443.1)
    assert b.height_source == "height_roof"
    assert len(b.rings) == 1
    assert len(b.rings[0]) == 5


def test_normalize_height_fallback():
    row = {**SAMPLE_FOOTPRINT_ROW, "height_roof": None, "num_floors": "10"}
    b = normalize_footprint(row, ANCHOR_LON, ANCHOR_LAT)
    assert b is not None
    assert b.height_source == "numfloors"
    assert b.height_ft == pytest.approx(10 * 11.48)


def test_normalize_missing_geom():
    row = {**SAMPLE_FOOTPRINT_ROW, "the_geom": None}
    assert normalize_footprint(row, ANCHOR_LON, ANCHOR_LAT) is None


def test_normalize_multipolygon():
    row = {
        **SAMPLE_FOOTPRINT_ROW,
        "the_geom": {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [
                        [-73.986, 40.748],
                        [-73.985, 40.748],
                        [-73.985, 40.747],
                        [-73.986, 40.747],
                        [-73.986, 40.748],
                    ]
                ]
            ],
        },
    }
    b = normalize_footprint(row, ANCHOR_LON, ANCHOR_LAT)
    assert b is not None
    assert len(b.rings) >= 1


def test_normalize_zoning_coloring():
    b = normalize_footprint(SAMPLE_FOOTPRINT_ROW, ANCHOR_LON, ANCHOR_LAT, "R8A")
    assert b is not None
    assert b.zoning_category == "R"
    assert b.color_hex == "#F5DEB3"


def test_normalize_commercial_color():
    b = normalize_footprint(SAMPLE_FOOTPRINT_ROW, ANCHOR_LON, ANCHOR_LAT, "C5-3")
    assert b is not None
    assert b.color_hex == "#4A90D9"
