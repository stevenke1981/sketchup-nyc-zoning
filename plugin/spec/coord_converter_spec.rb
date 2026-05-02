require "minitest/autorun"

module Geom
  class Point3d
    attr_reader :x, :y, :z
    def initialize(x, y, z); @x = x; @y = y; @z = z; end
  end
end

module NYCZoning
  PLUGIN_DIR = File.join(__dir__, "..", "sketchup_nyc_zoning")
end

require_relative "../sketchup_nyc_zoning/geo/coord_converter"

class CoordConverterTest < Minitest::Test
  M2I = NYCZoning::CoordConverter::METERS_TO_INCHES

  def test_meters_to_point_origin
    pt = NYCZoning::CoordConverter.meters_to_point(0, 0)
    assert_in_delta(0.0, pt.x, 0.001)
    assert_in_delta(0.0, pt.y, 0.001)
    assert_equal(0, pt.z)
  end

  def test_meters_to_point_values
    pt = NYCZoning::CoordConverter.meters_to_point(1.0, 2.0)
    assert_in_delta(M2I,       pt.x, 0.001)
    assert_in_delta(2 * M2I,   pt.y, 0.001)
  end

  def test_ring_to_points_length
    ring = [[0, 0], [1, 0], [1, 1], [0, 1]]
    pts  = NYCZoning::CoordConverter.ring_to_points(ring)
    assert_equal(4, pts.length)
  end

  def test_height_to_inches
    assert_in_delta(M2I * 10, NYCZoning::CoordConverter.height_to_inches(10.0), 0.001)
  end

  def test_round_trip_scale
    # 1 meter → inches → back to meters
    inches = NYCZoning::CoordConverter.height_to_inches(1.0)
    meters = inches * NYCZoning::CoordConverter::INCHES_TO_METERS
    assert_in_delta(1.0, meters, 0.0001)
  end
end
