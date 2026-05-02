from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock
from nyczone.geo.bbox import BBox
from nyczone.sources.socrata import fetch_dataset, DATASET_IDS

BBOX = BBox(-74.001, 40.747, -73.997, 40.751)


@pytest.mark.asyncio
async def test_fetch_single_page(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json=[{"bin": "1001", "heightroof": "100"}])
    pages = []
    async for page in fetch_dataset("footprints", BBOX):
        pages.append(page)
    assert len(pages) == 1
    assert pages[0][0]["bin"] == "1001"


@pytest.mark.asyncio
async def test_fetch_pagination(httpx_mock: HTTPXMock):
    from nyczone.config import settings

    full_page = [{"bin": str(i)} for i in range(settings.socrata_limit)]
    partial_page = [{"bin": "last"}]

    # First call returns full page, second returns partial
    httpx_mock.add_response(json=full_page)
    httpx_mock.add_response(json=partial_page)

    pages = []
    async for page in fetch_dataset("footprints", BBOX):
        pages.append(page)
    assert len(pages) == 2
    assert pages[1][0]["bin"] == "last"


@pytest.mark.asyncio
async def test_fetch_empty(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json=[])
    pages = []
    async for page in fetch_dataset("footprints", BBOX):
        pages.append(page)
    assert pages == []


@pytest.mark.asyncio
async def test_fetch_http_error_retries(httpx_mock: HTTPXMock):
    """Server errors trigger tenacity retry; after MAX retries a RetryError is raised."""
    from tenacity import RetryError

    # Add 5 error responses (exceeds MAX_RETRIES=5 stop)
    for _ in range(5):
        httpx_mock.add_response(status_code=503)

    with pytest.raises(RetryError):
        async for _ in fetch_dataset("footprints", BBOX):
            pass
