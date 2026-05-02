module NYCZoning
  BBox = Struct.new(:min_lon, :min_lat, :max_lon, :max_lat) do
    def center
      [
        (min_lon + max_lon) / 2.0,
        (min_lat + max_lat) / 2.0,
      ]
    end

    def to_mcp_params
      {
        min_lon: min_lon,
        min_lat: min_lat,
        max_lon: max_lon,
        max_lat: max_lat,
      }
    end
  end
end
