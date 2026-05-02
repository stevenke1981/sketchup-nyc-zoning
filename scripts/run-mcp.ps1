# Start NYC Zoning HTTP server on 127.0.0.1:8765 (Ruby plugin endpoint)
$root   = Split-Path $PSScriptRoot -Parent
$python = "$root\mcp-server\.venv\Scripts\python.exe"
$db     = "$root\data\cache\nyc.sqlite"

if (-not (Test-Path $python)) {
    Write-Error "Python venv not found. Run: scripts\bootstrap.ps1"
    exit 1
}

New-Item -ItemType Directory -Force -Path (Split-Path $db) | Out-Null

Write-Host "NYC Zoning HTTP server → http://127.0.0.1:8765" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop." -ForegroundColor Gray

$env:NYC_ZONING_DB_PATH = $db
& $python -m nyczone_mcp.http_server
