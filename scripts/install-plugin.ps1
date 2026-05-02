# Install SketchUp plugin into Plugins folder
$root       = Split-Path $PSScriptRoot -Parent
$pluginSrc  = "$root\plugin"

# Auto-detect SketchUp version (newest first)
$sketchupBase = "$env:AppData\SketchUp"
$versions = Get-ChildItem $sketchupBase -Directory -ErrorAction SilentlyContinue |
            Sort-Object Name -Descending

if (-not $versions) {
    Write-Error "No SketchUp installation found in $sketchupBase"
    exit 1
}

$version    = $versions[0].Name
$pluginsDir = "$sketchupBase\$version\SketchUp\Plugins"

Write-Host "Installing to: $pluginsDir" -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $pluginsDir | Out-Null

Copy-Item "$pluginSrc\sketchup-nyc-zoning.rb" $pluginsDir -Force
Copy-Item "$pluginSrc\sketchup_nyc_zoning" $pluginsDir -Recurse -Force

# Copy config if not already present
$configDst = "$pluginsDir\sketchup_nyc_zoning\..\config\config.json"
if (-not (Test-Path $configDst)) {
    Copy-Item "$pluginSrc\config\config.example.json" `
              "$pluginsDir\config\config.json" -Force
    Write-Host "Config copied — edit $pluginsDir\config\config.json to set bearer_token" -ForegroundColor Yellow
}

Write-Host "Plugin installed. Restart SketchUp to load." -ForegroundColor Green
