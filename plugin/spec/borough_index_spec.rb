require "minitest/autorun"

module NYCZoning
  PLUGIN_DIR = File.join(__dir__, "..", "sketchup_nyc_zoning")
end

require_relative "../sketchup_nyc_zoning/geo/bbox"
require_relative "../sketchup_nyc_zoning/geo/borough_index"

class BoroughIndexTest < Minitest::Test
  def test_all_boroughs_present
    %w[manhattan brooklyn queens bronx statenisland].each do |b|
      assert NYCZoning::BoroughIndex.bbox(b), "missing bbox for #{b}"
    end
  end

  def test_manhattan_bbox_reasonable
    b = NYCZoning::BoroughIndex.bbox("manhattan")
    assert b.min_lon < -73.9
    assert b.max_lat > 40.8
  end

  def test_unknown_borough_nil
    assert_nil NYCZoning::BoroughIndex.bbox("atlantis")
  end

  def test_case_insensitive
    assert NYCZoning::BoroughIndex.bbox("MANHATTAN")
  end
end
