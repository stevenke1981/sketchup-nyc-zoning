# Task List

## Phase 0: Foundations
- [ ] Repo skeleton + bootstrap script (`scripts/bootstrap.ps1`)
- [ ] `.gitignore`, `README.md`, `.editorconfig`
- [ ] `docs/DATA_DICTIONARY.md`
- [ ] `docs/COORDINATE_SYSTEMS.md`
- [ ] `docs/ARCHITECTURE.md`

## Phase 1: Data Pipeline MVP
- [ ] `pipeline/pyproject.toml` + deps (httpx, pyproj, shapely, pydantic, typer, tenacity)
- [ ] `pipeline/src/nyczone/sources/socrata.py` — async client with retry + $where bbox
- [ ] `pipeline/src/nyczone/models/building.py` — pydantic models
- [ ] `pipeline/src/nyczone/models/pluto.py`
- [ ] `pipeline/src/nyczone/models/zoning.py`
- [ ] `pipeline/src/nyczone/geo/transform.py` — pyproj 4326↔2263 + to_local_meters()
- [ ] `pipeline/src/nyczone/geo/bbox.py`
- [ ] `pipeline/src/nyczone/geo/spatial_join.py` — footprints × zoning (shapely STRtree)
- [ ] `pipeline/src/nyczone/normalize/footprints.py`
- [ ] `pipeline/src/nyczone/normalize/pluto.py`
- [ ] `pipeline/src/nyczone/normalize/zoning.py`
- [ ] `pipeline/src/nyczone/cache/sqlite_store.py` — SQLite + R-tree, 7-day TTL
- [ ] `pipeline/src/nyczone/export/geojson.py` — emit local_x_m/local_y_m + color hints
- [ ] `pipeline/src/nyczone/cli.py` — typer: fetch, build-cache, export
- [ ] `pipeline/tests/` — pytest 85% coverage target

## Phase 2: MCP Server
- [ ] `mcp-server/pyproject.toml` + deps (mcp, fastmcp, pydantic)
- [ ] `mcp-server/src/nyczone_mcp/server.py` — FastMCP + dual transport (stdio + HTTP:8765)
- [ ] `mcp-server/src/nyczone_mcp/adapter.py` — wraps nyczone pipeline
- [ ] `mcp-server/src/nyczone_mcp/schemas.py` — pydantic I/O schemas
- [ ] `mcp-server/src/nyczone_mcp/tools/query_buildings.py`
- [ ] `mcp-server/src/nyczone_mcp/tools/query_zoning_district.py`
- [ ] `mcp-server/src/nyczone_mcp/tools/query_pluto.py`
- [ ] `mcp-server/src/nyczone_mcp/tools/search_by_address.py`
- [ ] `mcp-server/src/nyczone_mcp/tools/get_borough_stats.py`
- [ ] `mcp-server/tests/` — pytest 85% coverage target

## Phase 3: SketchUp Ruby Plugin
- [ ] `plugin/sketchup-nyc-zoning.rb` — loader stub + SketchupExtension
- [ ] `plugin/sketchup_nyc_zoning/main.rb` — menu + toolbar registration
- [ ] `plugin/sketchup_nyc_zoning/ui/dialog.{rb,html,css,js}`
- [ ] `plugin/sketchup_nyc_zoning/ui/progress.rb` — cancelable progress bar
- [ ] `plugin/sketchup_nyc_zoning/net/http_client.rb` — Net::HTTP with retry
- [ ] `plugin/sketchup_nyc_zoning/net/mcp_client.rb` — JSON-RPC over HTTP
- [ ] `plugin/sketchup_nyc_zoning/geo/coord_converter.rb`
- [ ] `plugin/sketchup_nyc_zoning/geo/bbox.rb`
- [ ] `plugin/sketchup_nyc_zoning/geo/borough_index.rb` — static bbox table
- [ ] `plugin/sketchup_nyc_zoning/geo/zip_index.rb` — static bbox table
- [ ] `plugin/sketchup_nyc_zoning/model/geometry_builder.rb`
- [ ] `plugin/sketchup_nyc_zoning/model/attribute_tagger.rb`
- [ ] `plugin/sketchup_nyc_zoning/model/zoning_palette.rb`
- [ ] `plugin/sketchup_nyc_zoning/model/chunk_loader.rb`
- [ ] `plugin/sketchup_nyc_zoning/util/logger.rb`
- [ ] `plugin/sketchup_nyc_zoning/util/config.rb`
- [ ] `plugin/config/config.example.json`
- [ ] `plugin/spec/` — minitest 80% pure-logic coverage

## Phase 4: Edge Cases
- [ ] Degenerate footprint handling (self-intersection, zero-area, holes)
- [ ] Offline mode (fallback to local cache when MCP unreachable)
- [ ] Cancel + resume mid-load
- [ ] Layer toggle by zoning class
- [ ] Address-driven recenter

## Phase 5: Hardening
- [ ] Structured JSON logging with shared request_id
- [ ] `scripts/e2e-smoke.ps1` — boot MCP + validate round trip
- [ ] `scripts/install-plugin.ps1` — copy to SketchUp Plugins folder
- [ ] All docs finalized
