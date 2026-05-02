# Bootstrap: create venvs and install deps for pipeline + mcp-server
$root = Split-Path $PSScriptRoot -Parent

Write-Host "=== NYC Zoning Bootstrap ===" -ForegroundColor Cyan

# Pipeline
Write-Host "`n[1/2] Setting up pipeline..." -ForegroundColor Yellow
Push-Location "$root\pipeline"
uv venv .venv
uv pip install -e ".[dev]" --python .\.venv\Scripts\python.exe
Pop-Location

# MCP server (needs pipeline as editable dep)
Write-Host "`n[2/2] Setting up mcp-server..." -ForegroundColor Yellow
Push-Location "$root\mcp-server"
uv venv .venv
uv pip install -e "$root\pipeline" --python .\.venv\Scripts\python.exe
uv pip install -e ".[dev]" --python .\.venv\Scripts\python.exe
Pop-Location

# Data dirs
New-Item -ItemType Directory -Force -Path "$root\data\cache" | Out-Null
New-Item -ItemType Directory -Force -Path "$root\data\logs"  | Out-Null

Write-Host "`nDone! Next steps:" -ForegroundColor Green
Write-Host "  cd pipeline && .\.venv\Scripts\activate"
Write-Host "  nyczone fetch --bbox -74.001,40.747,-73.997,40.751 --out ..\data\cache\test.geojson"
