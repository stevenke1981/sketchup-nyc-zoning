# SketchUp NYC Zoning

Load real NYC zoning 3D models into SketchUp. Three components:

| Component | Tech | Purpose |
|-----------|------|---------|
| `plugin/` | Ruby | SketchUp extension — UI + 3D geometry builder |
| `pipeline/` | Python | Data pipeline — fetches, normalizes, caches NYC Open Data |
| `mcp-server/` | Python | MCP server — exposes zoning tools to Claude + Ruby plugin |

## Quick Start

```powershell
# 1. Bootstrap (creates venvs, installs deps)
.\scripts\bootstrap.ps1

# 2. Fetch data for Times Square area
cd pipeline
.\.venv\Scripts\activate
nyczone fetch --bbox -74.001,40.747,-73.997,40.751 --out ..\data\cache\times-square.geojson

# 3. Start MCP server
.\scripts\run-mcp.ps1

# 4. Install SketchUp plugin
.\scripts\install-plugin.ps1
```

## Data Sources

- [Building Footprints](https://data.cityofnewyork.us/resource/qrmh-6wdr.json) — NYC Open Data
- [MapPLUTO](https://data.cityofnewyork.us/resource/64uk-42ks.json) — DCP lot data
- [Zoning Districts](https://data.cityofnewyork.us/resource/6tn7-vhp3.json) — DCP

## Docs

- [PRD](docs/PRD.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Coordinate Systems](docs/COORDINATE_SYSTEMS.md)
- [Data Dictionary](docs/DATA_DICTIONARY.md)
- [Task List](docs/TASK_LIST.md)
- [Risks](docs/RISKS.md)
- [Development Setup](docs/DEVELOPMENT.md)
