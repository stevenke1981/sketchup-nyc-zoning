"""Integration test for pipeline.fetch_buildings using mocked Socrata.

Pipeline now: footprints (5zhs-2jue) + PLUTO (64uk-42ks lat/lon filter), joined by BBL.
"""
from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock
from nyczone.geo.bbox import BBox
from nyczone.pipeline import fetch_buildings

BBOX = BBox(-74.001, 40.747, -73.997, 40.751)

FOOTPRINT_ROW = {
    "bin": "1001001",
    "mappluto_bbl": "1007510076",   # links to PLUTO bbl
    "height_roof": "443.1",
    "num_floors": "102",
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

PLUTO_ROW = {
    "bbl": "1007510076.00000000",   # PLUTO BBL has decimal form
    "zonedist1": "R8A",
    "numfloors": "4",
    "yearbuilt": "1920",
    "address": "100 TEST ST",
    "landuse": "01",
}


@pytest.mark.asyncio
async def test_fetch_buildings_basic(httpx_mock: HTTPXMock):
    # Two requests in parallel: footprints + PLUTO
    httpx_mock.add_response(json=[FOOTPRINT_ROW])
    httpx_mock.add_response(json=[PLUTO_ROW])

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
    httpx_mock.add_response(json=[PLUTO_ROW])

    anchor_lon, anchor_lat = BBOX.center
    buildings = await fetch_buildings(BBOX, anchor_lon, anchor_lat)

    assert buildings[0].zoning_district == "R8A"
    assert buildings[0].color_hex == "#F5DEB3"
    assert buildings[0].address == "100 TEST ST"
    assert buildings[0].year_built == 1920


@pytest.mark.asyncio
async def test_fetch_buildings_no_pluto_match(httpx_mock: HTTPXMock):
    """Building with no matching PLUTO row → empty zoning, still returned."""
    httpx_mock.add_response(json=[FOOTPRINT_ROW])
    httpx_mock.add_response(json=[])   # empty PLUTO

    anchor_lon, anchor_lat = BBOX.center
    buildings = await fetch_buildings(BBOX, anchor_lon, anchor_lat)
    assert len(buildings) == 1
    assert buildings[0].zoning_district == ""


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
