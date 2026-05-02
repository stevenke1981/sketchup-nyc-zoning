from __future__ import annotations

import pytest
from nyczone.geo.bbox import BBox


def test_from_str_valid():
    b = BBox.from_str("-74.001,40.747,-73.997,40.751")
    assert b.min_lon == pytest.approx(-74.001)
    assert b.max_lat == pytest.approx(40.751)


def test_from_str_invalid():
    with pytest.raises(ValueError):
        BBox.from_str("1,2,3")


def test_center():
    b = BBox(-74.0, 40.0, -73.0, 41.0)
    lon, lat = b.center
    assert lon == pytest.approx(-73.5)
    assert lat == pytest.approx(40.5)


def test_socrata_where():
    b = BBox(-74.001, 40.747, -73.997, 40.751)
    where = b.to_socrata_where()
    assert "within_box" in where
    assert "40.747" in where
    assert "-74.001" in where


def test_area():
    b = BBox(0.0, 0.0, 1.0, 1.0)
    assert b.area_deg2() == pytest.approx(1.0)
