"""SQLite cache with R-tree spatial index for buildings and zoning data."""
from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path

from nyczone.config import settings

DDL = """
CREATE TABLE IF NOT EXISTS buildings (
    id          INTEGER PRIMARY KEY,
    bbox_hash   TEXT NOT NULL UNIQUE,
    data        TEXT NOT NULL,
    fetched_at  INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS buildings_rtree (
    id          INTEGER PRIMARY KEY,
    min_lon REAL, max_lon REAL,
    min_lat REAL, max_lat REAL
);

CREATE TABLE IF NOT EXISTS zoning (
    id          INTEGER PRIMARY KEY,
    data        TEXT NOT NULL,
    fetched_at  INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_buildings_hash ON buildings(bbox_hash);
"""


def _conn(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.executescript(DDL)
    conn.commit()
    return conn


def _now() -> int:
    return int(time.time())


def cache_buildings(bbox_hash: str, features: list[dict]) -> None:  # type: ignore[type-arg]
    with _conn(settings.db_path) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO buildings(bbox_hash, data, fetched_at) VALUES (?,?,?)",
            (bbox_hash, json.dumps(features), _now()),
        )


def load_buildings(bbox_hash: str, ttl_days: int | None = None) -> list[dict] | None:  # type: ignore[type-arg]
    ttl = (ttl_days or settings.footprints_ttl_days) * 86400
    with _conn(settings.db_path) as conn:
        row = conn.execute(
            "SELECT data, fetched_at FROM buildings WHERE bbox_hash=?", (bbox_hash,)
        ).fetchone()
    if not row:
        return None
    data, fetched_at = row
    if _now() - fetched_at > ttl:
        return None
    return json.loads(data)
