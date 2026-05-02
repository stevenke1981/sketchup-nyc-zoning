"""Unit tests for MCP tools."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from pytest_httpx import HTTPXMock


# ── query_buildings ──────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_query_buildings_returns_feature_collection():
    from nyczone_mcp.tools.query_buildings import query_buildings

    mock_fc = {
        "type": "FeatureCollection",
        "features": [{"type": "Feature", "properties": {"bbl": "1001"}, "geometry": None}],
    }
    with patch(
        "nyczone_mcp.tools.query_buildings.fetch_buildings", new_callable=AsyncMock
    ) as mock_fetch, patch(
        "nyczone_mcp.tools.query_buildings.buildings_to_geojson", return_value=mock_fc
    ):
        mock_fetch.return_value = [object()]
        result = await query_buildings(-74.001, 40.747, -73.997, 40.751, limit=10)

    assert result["type"] == "FeatureCollection"
    assert len(result["features"]) == 1


# ── query_zoning_district ────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_query_zoning_found(httpx_mock: HTTPXMock):
    from nyczone_mcp.tools.query_zoning_district import query_zoning_district

    httpx_mock.add_response(json=[{"zonedist": "C5-3", "label": "C5-3"}])
    result = await query_zoning_district(-73.9857, 40.7484)
    assert result["zoning_district"] == "C5-3"


@pytest.mark.asyncio
async def test_query_zoning_not_found(httpx_mock: HTTPXMock):
    from nyczone_mcp.tools.query_zoning_district import query_zoning_district

    httpx_mock.add_response(json=[])
    result = await query_zoning_district(-73.9857, 40.7484)
    assert result["zoning_district"] is None


# ── search_by_address ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_search_by_address_found(httpx_mock: HTTPXMock):
    from nyczone_mcp.tools.search_by_address import search_by_address

    httpx_mock.add_response(
        json={
            "features": [
                {
                    "geometry": {"coordinates": [-73.9857, 40.7484]},
                    "properties": {
                        "label": "350 5th Ave, New York, NY",
                        "pad_bbl": "1008880001",
                    },
                }
            ]
        }
    )
    result = await search_by_address("350 5th Ave, New York")
    assert result["lon"] == pytest.approx(-73.9857)
    assert "suggested_bbox" in result


@pytest.mark.asyncio
async def test_search_by_address_not_found(httpx_mock: HTTPXMock):
    from nyczone_mcp.tools.search_by_address import search_by_address

    httpx_mock.add_response(json={"features": []})
    result = await search_by_address("nowhere special")
    assert "error" in result


# ── get_borough_stats ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_borough_stats_valid(httpx_mock: HTTPXMock):
    from nyczone_mcp.tools.get_borough_stats import get_borough_stats

    httpx_mock.add_response(
        json=[{"total": "1234", "avg_height_ft": "75.5"}]
    )
    result = await get_borough_stats("manhattan")
    assert result["total_buildings"] == 1234
    assert result["avg_height_ft"] == pytest.approx(75.5)


@pytest.mark.asyncio
async def test_get_borough_stats_invalid():
    from nyczone_mcp.tools.get_borough_stats import get_borough_stats

    result = await get_borough_stats("atlantis")
    assert "error" in result
