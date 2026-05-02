# Install NYC Zoning plugin into SketchUp Plugins folder
$root      = Split-Path $PSScriptRoot -Parent
$pluginSrc = "$root\plugin"

# 1. Try AppData\Roaming\SketchUp (exists after first SketchUp launch)
$sketchupBase = "$env:AppData\SketchUp"
$versions = Get-ChildItem $sketchupBase -Directory -ErrorAction SilentlyContinue |
            Sort-Object Name -Descending

if ($versions) {
    $pluginsDir = "$sketchupBase\$($versions[0].Name)\SketchUp\Plugins"
} else {
    # 2. SketchUp not yet run — detect installed version from Program Files
    $pfBase    = "C:\Program Files\SketchUp"
    $pfVersions = Get-ChildItem $pfBase -Directory -ErrorAction SilentlyContinue |
                  Sort-Object Name -Descending
    if (-not $pfVersions) {
        Write-Error "SketchUp not found in $pfBase. Install SketchUp first."
        exit 1
    }
    $versionName = $pfVersions[0].Name   # e.g. "SketchUp 2026"
    $pluginsDir  = "$sketchupBase\$versionName\SketchUp\Plugins"
    Write-Host "SketchUp AppData not yet created — will pre-populate: $pluginsDir" -ForegroundColor Yellow
}

Write-Host "Installing to: $pluginsDir" -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $pluginsDir | Out-Null

Copy-Item "$pluginSrc\sketchup-nyc-zoning.rb"    $pluginsDir -Force
Copy-Item "$pluginSrc\sketchup_nyc_zoning"        $pluginsDir -Recurse -Force

# Copy config (only if not already customised)
$configDir = "$pluginsDir\config"
$configDst = "$configDir\config.json"
if (-not (Test-Path $configDst)) {
    New-Item -ItemType Directory -Force -Path $configDir | Out-Null
    Copy-Item "$pluginSrc\config\config.example.json" $configDst -Force
    Write-Host "Config created at: $configDst" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Plugin installed successfully." -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Run:  .\scripts\run-mcp.ps1      (keep this terminal open)" -ForegroundColor White
Write-Host "  2. Open SketchUp 2026" -ForegroundColor White
Write-Host "  3. Menu: Plugins → NYC Zoning → Load Model" -ForegroundColor White
