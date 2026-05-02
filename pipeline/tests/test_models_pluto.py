from __future__ import annotations

import pytest
from nyczone.models.pluto import Pluto
from nyczone.normalize.pluto import normalize_pluto


def test_pluto_defaults():
    p = Pluto()
    assert p.bbl == ""
    assert p.year_built == 0
    assert p.far == 0.0


def test_pluto_coerce_int():
    p = Pluto(year_built="1931", numfloors="102")
    assert p.year_built == 1931
    assert p.numfloors == 102


def test_pluto_coerce_float():
    p = Pluto(far="21.6", lot_area_sqft="32,000")  # comma should fail gracefully
    assert p.far == pytest.approx(21.6)
    assert p.lot_area_sqft == 0.0  # coercion fails → default


def test_pluto_coerce_invalid():
    p = Pluto(year_built="not_a_year")
    assert p.year_built == 0


def test_normalize_pluto_row():
    row = {
        "bbl": "1008880001",
        "address": "350 5TH AVE",
        "zipcode": "10118",
        "borough": "MN",
        "yearbuilt": "1931",
        "numfloors": "102",
        "landuse": "05",
        "builtfar": "21.6",
        "lotarea": "79288",
        "bldgarea": "2768591",
    }
    p = normalize_pluto(row)
    assert p.bbl == "1008880001"
    assert p.year_built == 1931
    assert p.far == pytest.approx(21.6)


def test_normalize_pluto_missing_fields():
    p = normalize_pluto({})
    assert p.bbl == ""
    assert p.year_built == 0
