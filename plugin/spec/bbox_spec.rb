require "minitest/autorun"

# Stub the Geom module so coord_converter loads outside SketchUp
module Geom
  class Point3d
    attr_reader :x, :y, :z
    def initialize(x, y, z); @x = x; @y = y; @z = z; end
  end
end

module NYCZoning
  PLUGIN_DIR = File.join(__dir__, "..", "sketchup_nyc_zoning")
end

require_relative "../sketchup_nyc_zoning/geo/bbox"

class BBoxTest < Minitest::Test
  def test_center
    b = NYCZoning::BBox.new(-74.0, 40.0, -73.0, 41.0)
    lon, lat = b.center
    assert_in_delta(-73.5, lon, 0.001)
    assert_in_delta(40.5,  lat, 0.001)
  end

  def test_mcp_params_keys
    b = NYCZoning::BBox.new(-74.001, 40.747, -73.997, 40.751)
    p = b.to_mcp_params
    assert p.key?(:min_lon)
    assert p.key?(:max_lat)
  end
end
