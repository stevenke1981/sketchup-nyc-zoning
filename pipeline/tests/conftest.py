"""Shared pytest fixtures."""
from __future__ import annotations

import pytest

# Simple Manhattan bbox for tests
TIMES_SQUARE_BBOX_STR = "-74.001,40.747,-73.997,40.751"
ANCHOR_LON = -73.999
ANCHOR_LAT = 40.749

SAMPLE_FOOTPRINT_ROW = {
    "bin": "1001001",
    "heightroof": "443.1",
    "numfloors": "102",
    "the_geom": {
        "type": "Polygon",
        "coordinates": [
            [
                [-73.9857, 40.7484],
                [-73.9850, 40.7484],
                [-73.9850, 40.7480],
                [-73.9857, 40.7480],
                [-73.9857, 40.7484],
            ]
        ],
    },
}

SAMPLE_ZONING_ROW = {
    "zonedist": "C5-3",
    "label": "C5-3",
    "the_geom": {
        "type": "Polygon",
        # Wide enough to contain the SAMPLE_FOOTPRINT_ROW centroid (~-73.985, 40.748)
        "coordinates": [
            [
                [-74.002, 40.744],
                [-73.980, 40.744],
                [-73.980, 40.754],
                [-74.002, 40.754],
                [-74.002, 40.744],
            ]
        ],
    },
}
