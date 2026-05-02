# Start MCP server (stdio + HTTP on 127.0.0.1:8765)
$root   = Split-Path $PSScriptRoot -Parent
$python = "$root\mcp-server\.venv\Scripts\python.exe"
$db     = "$root\data\cache\nyc.sqlite"

Write-Host "Starting NYC Zoning MCP server on port 8765..." -ForegroundColor Cyan
$env:NYC_ZONING_DB_PATH = $db
& $python -m nyczone_mcp.server
