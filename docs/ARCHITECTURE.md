# Architecture

## System Diagram

```
+--------------------------------------------------------------------------+
|                              SketchUp 2022+                              |
|  +---------------------------------------------------------------------+ |
|  |  Ruby Plugin                                                        | |
|  |  HtmlDialog → Selection → HTTP Client → Geometry Builder           | |
|  |                                  ↓              ↓                  | |
|  |                          Coord Converter   Attribute Tagger        | |
|  +----------------------------------|----------------------------------+ |
+--------------------------------------|-----------------------------------+
                                       | HTTP JSON-RPC (localhost:8765)
                                       ↓
+--------------------------------------------------------------------------+
|                     MCP Server (Python, FastMCP)                         |
|  stdio transport ←→ [query_buildings | query_zoning | query_pluto |      |
|                       search_by_address | get_borough_stats]             |
|                                       ↓ pipeline adapter                 |
+--------------------------------------------------------------------------+
                                       ↓
+--------------------------------------------------------------------------+
|                     Data Pipeline (nyczone package)                      |
|  Socrata Fetcher → Normalizer → Coord Transform → Spatial Join → Cache   |
+--------------------------------------------------------------------------+
                                       ↓
                         NYC Open Data (Socrata API)
```

## Transport

- **Ruby Plugin → MCP**: Streamable HTTP on `127.0.0.1:8765` (plain JSON-RPC, no MCP SDK in Ruby)
- **Claude Desktop → MCP**: stdio (standard MCP)

## Key Decision: Projection in Pipeline, Not Plugin

The pipeline emits `local_x_m` / `local_y_m` per vertex (anchor-relative meters).  
Ruby consumes pure Cartesian coordinates — no native gems needed in SketchUp.

## Component Boundaries

```
plugin/      → SketchUp UI + 3D geometry only; no business logic
pipeline/    → All data fetching, normalization, projection, caching
mcp-server/  → Thin adapter: MCP protocol ↔ pipeline calls
```
