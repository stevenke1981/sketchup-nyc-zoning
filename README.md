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

# 2. Install SketchUp plugin
.\scripts\install-plugin.ps1

# 3. Start MCP server — keep this terminal open the entire session
.\scripts\run-mcp.ps1

# 4. Open SketchUp 2026 → Extensions → NYC Zoning - Load Model
```

> **Important:** `run-mcp.ps1` must stay running while SketchUp is open.
> Open it in a **dedicated PowerShell window** and leave it running.
> Every time you restart SketchUp, restart this script first.
> If you see `Net::ReadTimeout` in the plugin, the server has stopped — rerun this script.

## Data Sources

- [Building Footprints](https://data.cityofnewyork.us/resource/qrmh-6wdr.json) — NYC Open Data
- [MapPLUTO](https://data.cityofnewyork.us/resource/64uk-42ks.json) — DCP lot data
- [Zoning Districts](https://data.cityofnewyork.us/resource/6tn7-vhp3.json) — DCP

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `Net::ReadTimeout` in plugin | MCP server not running | Run `.\scripts\run-mcp.ps1` in a dedicated terminal |
| Buildings appear upside-down | `pushpull` direction bug | Fixed in v1.0.1 — reinstall plugin |
| `NYC Zoning` missing from Extensions menu | Plugin not installed | Run `.\scripts\install-plugin.ps1`, restart SketchUp |

## Docs

- [PRD](docs/PRD.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Coordinate Systems](docs/COORDINATE_SYSTEMS.md)
- [Data Dictionary](docs/DATA_DICTIONARY.md)
- [Task List](docs/TASK_LIST.md)
- [Risks](docs/RISKS.md)
- [Development Setup](docs/DEVELOPMENT.md)
