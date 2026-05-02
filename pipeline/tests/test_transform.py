from __future__ import annotations

import pytest
from nyczone.geo.transform import (
    ring_to_local_meters,
    state_plane_to_wgs84,
    to_local_meters,
    wgs84_to_state_plane,
)

# Empire State Building
ESB_LON, ESB_LAT = -73.9857, 40.7484


def test_round_trip_wgs84():
    x, y = wgs84_to_state_plane(ESB_LON, ESB_LAT)
    lon, lat = state_plane_to_wgs84(x, y)
    assert lon == pytest.approx(ESB_LON, abs=1e-5)
    assert lat == pytest.approx(ESB_LAT, abs=1e-5)


def test_anchor_origin():
    x, y = to_local_meters(ESB_LON, ESB_LAT, ESB_LON, ESB_LAT)
    assert x == pytest.approx(0.0, abs=0.01)
    assert y == pytest.approx(0.0, abs=0.01)


def test_local_meters_direction():
    # A point slightly north of the anchor should have positive y
    x, y = to_local_meters(ESB_LON, ESB_LAT + 0.001, ESB_LON, ESB_LAT)
    assert y > 0
    # A point slightly east should have positive x
    x2, _ = to_local_meters(ESB_LON + 0.001, ESB_LAT, ESB_LON, ESB_LAT)
    assert x2 > 0


def test_ring_conversion_length():
    ring = [
        [ESB_LON, ESB_LAT],
        [ESB_LON + 0.001, ESB_LAT],
        [ESB_LON + 0.001, ESB_LAT + 0.001],
        [ESB_LON, ESB_LAT],
    ]
    result = ring_to_local_meters(ring, ESB_LON, ESB_LAT)
    assert len(result) == 4
    # First point = anchor → (0, 0)
    assert result[0][0] == pytest.approx(0.0, abs=0.01)
    assert result[0][1] == pytest.approx(0.0, abs=0.01)


def test_100m_offset():
    # ~0.0009 deg ≈ 100m latitude
    x, y = to_local_meters(ESB_LON, ESB_LAT + 0.0009, ESB_LON, ESB_LAT)
    assert 90 < y < 110  # roughly 100 m
