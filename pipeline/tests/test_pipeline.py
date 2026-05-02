"""Integration test for pipeline.fetch_buildings using mocked Socrata."""
from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock
from nyczone.geo.bbox import BBox
from nyczone.pipeline import fetch_buildings

BBOX = BBox(-74.001, 40.747, -73.997, 40.751)

FOOTPRINT_ROW = {
    "bin": "1001001",
    "heightroof": "443.1",
    "numfloors": "102",
    "the_geom": {
        "type": "Polygon",
        "coordinates": [
            [
                [-73.9990, 40.7490],
                [-73.9985, 40.7490],
                [-73.9985, 40.7486],
                [-73.9990, 40.7486],
                [-73.9990, 40.7490],
            ]
        ],
    },
}

ZONING_ROW = {
    "zonedist": "R8A",
    "label": "R8A",
    "the_geom": {
        "type": "Polygon",
        "coordinates": [
            [
                [-74.005, 40.744],
                [-73.993, 40.744],
                [-73.993, 40.755],
                [-74.005, 40.755],
                [-74.005, 40.744],
            ]
        ],
    },
}


@pytest.mark.asyncio
async def test_fetch_buildings_basic(httpx_mock: HTTPXMock):
    # Two requests: footprints + zoning (in parallel)
    httpx_mock.add_response(json=[FOOTPRINT_ROW])
    httpx_mock.add_response(json=[ZONING_ROW])

    anchor_lon, anchor_lat = BBOX.center
    buildings = await fetch_buildings(BBOX, anchor_lon, anchor_lat)

    assert len(buildings) == 1
    b = buildings[0]
    assert b.bin == "1001001"
    assert b.height_ft == pytest.approx(443.1)
    assert len(b.rings[0]) == 5


@pytest.mark.asyncio
async def test_fetch_buildings_zoning_tagged(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json=[FOOTPRINT_ROW])
    httpx_mock.add_response(json=[ZONING_ROW])

    anchor_lon, anchor_lat = BBOX.center
    buildings = await fetch_buildings(BBOX, anchor_lon, anchor_lat)

    assert buildings[0].zoning_district == "R8A"
    assert buildings[0].color_hex == "#F5DEB3"


@pytest.mark.asyncio
async def test_fetch_buildings_empty(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json=[])
    httpx_mock.add_response(json=[])

    anchor_lon, anchor_lat = BBOX.center
    buildings = await fetch_buildings(BBOX, anchor_lon, anchor_lat)
    assert buildings == []


@pytest.mark.asyncio
async def test_fetch_buildings_skips_invalid_geom(httpx_mock: HTTPXMock):
    bad_row = {**FOOTPRINT_ROW, "the_geom": None}
    httpx_mock.add_response(json=[bad_row])
    httpx_mock.add_response(json=[])

    anchor_lon, anchor_lat = BBOX.center
    buildings = await fetch_buildings(BBOX, anchor_lon, anchor_lat)
    assert buildings == []
