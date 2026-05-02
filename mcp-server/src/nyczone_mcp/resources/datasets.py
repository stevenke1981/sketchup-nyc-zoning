"""MCP resources: expose cached dataset info."""
from __future__ import annotations

from nyczone.geo.borough_bboxes import BOROUGH_BBOXES

BOROUGH_RESOURCE = {
    "boroughs": {
        name: {"bbox": [b.min_lon, b.min_lat, b.max_lon, b.max_lat]}
        for name, b in BOROUGH_BBOXES.items()
    },
    "datasets": {
        "footprints": "qrmh-6wdr",
        "pluto": "64uk-42ks",
        "zoning": "6tn7-vhp3",
    },
}
