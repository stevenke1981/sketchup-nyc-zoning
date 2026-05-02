from __future__ import annotations

import json
import sqlite3
import time

import pytest
from nyczone.cache import sqlite_store as store
from nyczone.config import settings


@pytest.fixture(autouse=True)
def tmp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "db_path", tmp_path / "test.sqlite")
    monkeypatch.setattr(settings, "footprints_ttl_days", 7)


def test_cache_and_load():
    features = [{"bin": "1", "height_ft": 100.0}]
    store.cache_buildings("hash1", features)
    assert store.load_buildings("hash1") == features


def test_load_missing_returns_none():
    assert store.load_buildings("nonexistent") is None


def _insert_with_ts(bbox_hash, data, ts):
    store.cache_buildings("_init", [])  # ensure schema exists
    conn = sqlite3.connect(str(settings.db_path))
    conn.execute(
        "INSERT OR REPLACE INTO buildings(bbox_hash, data, fetched_at) VALUES (?,?,?)",
        (bbox_hash, json.dumps(data), ts),
    )
    conn.commit()
    conn.close()


def test_load_expired_returns_none():
    _insert_with_ts("hash_exp", [{"v": 1}], int(time.time()) - 8 * 86400)
    assert store.load_buildings("hash_exp") is None


def test_load_fresh_returns_data():
    store.cache_buildings("hash_fresh", [{"v": 99}])
    assert store.load_buildings("hash_fresh") == [{"v": 99}]


def test_overwrite_updates_data():
    store.cache_buildings("hash3", [{"v": 1}])
    store.cache_buildings("hash3", [{"v": 2}])
    assert store.load_buildings("hash3") == [{"v": 2}]


def test_custom_ttl():
    _insert_with_ts("hash_2d", [{"x": 1}], int(time.time()) - 2 * 86400)
    assert store.load_buildings("hash_2d", ttl_days=1) is None
    assert store.load_buildings("hash_2d", ttl_days=3) == [{"x": 1}]
