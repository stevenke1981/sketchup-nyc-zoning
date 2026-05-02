# Development Setup (Windows 11)

## Prerequisites

- Python 3.11+ (`winget install Python.Python.3.11`)
- uv (`pip install uv`)
- SketchUp 2022+ installed
- Git

## Bootstrap

```powershell
cd C:\Users\steven\sketchup-nyc-zoning
.\scripts\bootstrap.ps1
```

This creates:
- `pipeline\.venv\` with nyczone + dev deps
- `mcp-server\.venv\` with nyczone_mcp + dev deps

## Pipeline Development

```powershell
cd pipeline
.\.venv\Scripts\activate

# Fetch Times Square (small test area)
nyczone fetch --bbox -74.001,40.747,-73.997,40.751 --out ..\data\cache\test.geojson

# Build borough cache (takes ~5 min, ~150k buildings)
nyczone build-cache --borough manhattan

# Run tests
pytest tests/ -v --cov=nyczone
```

## MCP Server

```powershell
# Start server (stdio + HTTP on 8765)
.\scripts\run-mcp.ps1

# Test with curl
curl -X POST http://localhost:8765 `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer <token>" `
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

## Claude Desktop Integration

Add to `%AppData%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "nyc-zoning": {
      "command": "C:\\Users\\steven\\sketchup-nyc-zoning\\mcp-server\\.venv\\Scripts\\python.exe",
      "args": ["-m", "nyczone_mcp.server"],
      "env": {
        "NYC_ZONING_DB": "C:\\Users\\steven\\sketchup-nyc-zoning\\data\\cache\\nyc.sqlite"
      }
    }
  }
}
```

## SketchUp Plugin

```powershell
# Install (copies to SketchUp Plugins folder)
.\scripts\install-plugin.ps1

# Plugin config
cp plugin\config\config.example.json plugin\config\config.json
# Edit config.json: set mcp_url, bearer_token
```

## NYC Open Data App Token

Register at https://data.cityofnewyork.us/profile/app_tokens
Set as env var:
```powershell
$env:NYC_APP_TOKEN = "your_token_here"
```
Without token: 1000 req/hr limit. With token: 2000+ req/hr.
