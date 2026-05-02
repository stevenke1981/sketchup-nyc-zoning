from __future__ import annotations

import pytest
from conftest import ANCHOR_LAT, ANCHOR_LON, SAMPLE_FOOTPRINT_ROW, SAMPLE_ZONING_ROW
from nyczone.geo.spatial_join import build_zoning_tree, tag_buildings_with_zoning
from nyczone.normalize.footprints import normalize_footprint
from nyczone.normalize.zoning import normalize_zoning


@pytest.fixture()
def district():
    return normalize_zoning(SAMPLE_ZONING_ROW)


@pytest.fixture()
def building():
    return normalize_footprint(SAMPLE_FOOTPRINT_ROW, ANCHOR_LON, ANCHOR_LAT)


def test_tree_builds(district):
    tree, valid = build_zoning_tree([district])
    assert len(valid) == 1


def test_tag_assigns_zoning(building, district):
    tagged = tag_buildings_with_zoning([building], [district], ANCHOR_LON, ANCHOR_LAT)
    assert len(tagged) == 1
    # Building centroid is inside the large test zoning polygon
    assert tagged[0].zoning_district == "C5-3"
    assert tagged[0].color_hex == "#4A90D9"


def test_tag_no_districts(building):
    tagged = tag_buildings_with_zoning([building], [], ANCHOR_LON, ANCHOR_LAT)
    assert tagged[0].zoning_district == ""


def test_tag_outside_all_districts(building):
    far_district = normalize_zoning(
        {
            "zonedist": "M1-1",
            "label": "M1-1",
            "the_geom": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-74.100, 40.600],
                        [-74.090, 40.600],
                        [-74.090, 40.610],
                        [-74.100, 40.610],
                        [-74.100, 40.600],
                    ]
                ],
            },
        }
    )
    tagged = tag_buildings_with_zoning([building], [far_district], ANCHOR_LON, ANCHOR_LAT)
    assert tagged[0].zoning_district == ""
