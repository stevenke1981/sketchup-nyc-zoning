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

## Phase 6: Taiwan Support

目標：支援台灣縣市建物 3D 模型載入，架構與 NYC pipeline 平行。

### 資料來源
- [ ] 研究內政部國土測繪中心 WFS API（建物輪廓圖徵資料）
- [ ] 研究內政部營建署城鄉發展分署都市計畫分區 API
- [ ] 評估 OpenStreetMap Overpass API 作為建物高度補充來源
      （台北、新北、台中、高雄覆蓋率較完整）

### Pipeline
- [ ] `pipeline/src/twzone/` — 台灣 pipeline 套件（與 nyczone 平行）
- [ ] `pipeline/src/twzone/sources/nlsc.py` — 國土測繪中心 WFS client
- [ ] `pipeline/src/twzone/sources/overpass.py` — OSM Overpass API client
- [ ] `pipeline/src/twzone/sources/urban_plan.py` — 都市計畫分區 API client
- [ ] `pipeline/src/twzone/geo/transform.py` — TWD97 (EPSG:3826) ↔ WGS84 轉換
- [ ] `pipeline/src/twzone/normalize/buildings.py` — 樓層數 × 3m 估算建物高度
- [ ] `pipeline/src/twzone/normalize/zoning.py` — 住宅區/商業區/工業區色碼對應
- [ ] `pipeline/src/twzone/export/geojson.py` — 輸出 local_x_m/local_y_m 格式

### MCP Server
- [ ] `mcp-server/src/nyczone_mcp/tools/tw_query_buildings.py` — bbox 查詢建物
- [ ] `mcp-server/src/nyczone_mcp/tools/tw_query_zoning.py` — 都市計畫分區查詢
- [ ] `mcp-server/src/nyczone_mcp/tools/tw_search_by_address.py` — 地址轉座標

### SketchUp Plugin
- [ ] `plugin/sketchup_nyc_zoning/geo/tw_city_index.rb` — 縣市 bbox 靜態表
      （台北市、新北市、台中市、台南市、高雄市、桃園市）
- [ ] Plugin UI 新增 Taiwan 分頁，支援縣市下拉選單

### 研究事項
- [ ] 確認國土測繪中心 WFS 開放授權條款
- [ ] 確認都市計畫分區 API 是否有 bbox 空間查詢支援
- [ ] 評估 TWD97 本島坐標系 vs WGS84 精度差異對 SketchUp 的影響
