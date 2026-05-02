"""HTTP bridge on 127.0.0.1:8765 — accepts JSON-RPC from the SketchUp Ruby plugin."""
from __future__ import annotations

import json
import logging
from typing import Any

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from nyczone.export.geojson import buildings_to_geojson
from nyczone.geo.bbox import BBox
from nyczone.pipeline import fetch_buildings

logger = logging.getLogger("nyczone.http")

HOST = "127.0.0.1"
PORT = 8765


async def _query_buildings(args: dict[str, Any]) -> dict[str, Any]:
    bbox = BBox(
        float(args["min_lon"]),
        float(args["min_lat"]),
        float(args["max_lon"]),
        float(args["max_lat"]),
    )
    anchor_lon, anchor_lat = bbox.center
    buildings = await fetch_buildings(bbox, anchor_lon, anchor_lat)
    limit = int(args.get("limit", 2000))
    buildings = buildings[:limit]
    return buildings_to_geojson(buildings, anchor_lon, anchor_lat)


_TOOLS: dict[str, Any] = {
    "query_buildings": _query_buildings,
}


async def handle(request: Request) -> JSONResponse:
    try:
        data: dict[str, Any] = await request.json()
    except Exception:
        return JSONResponse({"error": "invalid JSON"}, status_code=400)

    req_id = data.get("id", 1)
    params = data.get("params", {})
    name = str(params.get("name", ""))
    args = params.get("arguments", {})

    logger.info("tool=%s id=%s", name, req_id)

    fn = _TOOLS.get(name)
    if fn is None:
        return JSONResponse(
            {"jsonrpc": "2.0", "id": req_id, "error": {"message": f"Unknown tool: {name}"}},
            status_code=404,
        )

    try:
        result = await fn(args)
    except Exception as exc:
        logger.exception("tool %s failed", name)
        return JSONResponse(
            {"jsonrpc": "2.0", "id": req_id, "error": {"message": str(exc)}},
            status_code=500,
        )

    return JSONResponse({
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {"content": [{"type": "text", "text": json.dumps(result)}]},
    })


app = Starlette(routes=[Route("/", handle, methods=["POST"])])


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logger.info("NYC Zoning HTTP server starting on %s:%s", HOST, PORT)
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")


if __name__ == "__main__":
    main()
