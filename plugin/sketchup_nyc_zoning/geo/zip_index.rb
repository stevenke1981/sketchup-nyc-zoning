module NYCZoning
  module ZipIndex
    # Representative bboxes for key NYC ZIP codes (delta ~0.01 deg each side)
    BBOXES = {
      "10001" => BBox.new(-74.004, 40.742, -73.984, 40.757),  # Midtown West
      "10002" => BBox.new(-74.002, 40.710, -73.982, 40.725),  # Lower East Side
      "10036" => BBox.new(-74.004, 40.755, -73.984, 40.770),  # Times Square
      "10022" => BBox.new(-73.979, 40.755, -73.959, 40.770),  # Midtown East
      "10007" => BBox.new(-74.020, 40.705, -74.000, 40.720),  # City Hall
      "11201" => BBox.new(-74.010, 40.685, -73.990, 40.700),  # Brooklyn Heights
      "11215" => BBox.new(-73.994, 40.658, -73.974, 40.673),  # Park Slope
      "11101" => BBox.new(-73.956, 40.740, -73.936, 40.755),  # LIC Queens
    }.freeze

    def self.bbox(zip)
      BBOXES[zip.to_s.strip]
    end
  end
end
