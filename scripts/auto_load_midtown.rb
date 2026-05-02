# Auto-load Midtown Manhattan buildings on SketchUp startup
# Targets: Empire State Building, Chrysler Building, and surrounding blocks
# BBox: 40.744°N–40.758°N, 73.995°W–73.978°W

MIDTOWN_BBOX = {
  min_lon: -73.9950,
  min_lat:  40.7440,
  max_lon: -73.9780,
  max_lat:  40.7580,
  limit:    600,
}.freeze

UI.start_timer(2.5, false) do
  begin
    Sketchup.status_text = "NYC Zoning: connecting to server..."

    client  = NYCZoning::McpClient.new
    raw     = client.call_tool("query_buildings", MIDTOWN_BBOX)
    geojson = JSON.parse(raw)
    features = geojson["features"] || []

    if features.empty?
      Sketchup.status_text = "NYC Zoning: no buildings returned."
      next
    end

    Sketchup.status_text = "NYC Zoning: loading #{features.length} buildings..."

    model  = Sketchup.active_model
    loader = NYCZoning::ChunkLoader.new(features, model, chunk_size: 100)
    loader.run do |done, total|
      Sketchup.status_text = "NYC Zoning: #{done}/#{total} buildings..."
    end

    # Fit camera to show all loaded geometry
    model.active_view.zoom_extents

    Sketchup.status_text =
      "NYC Zoning: #{loader.loaded} buildings loaded, #{loader.skipped} skipped."
  rescue StandardError => e
    Sketchup.status_text = "NYC Zoning error: #{e.message}"
  end
end
