require "minitest/autorun"

module Sketchup; end
module NYCZoning
  PLUGIN_DIR = File.join(__dir__, "..", "sketchup_nyc_zoning")
end

require_relative "../sketchup_nyc_zoning/model/zoning_palette"

class ZoningPaletteTest < Minitest::Test
  def test_residential
    assert_equal "F5DEB3", NYCZoning::ZoningPalette.color_for("R8A")
  end

  def test_commercial
    assert_equal "4A90D9", NYCZoning::ZoningPalette.color_for("C5-3")
  end

  def test_manufacturing
    assert_equal "C0392B", NYCZoning::ZoningPalette.color_for("M1-5")
  end

  def test_park
    assert_equal "27AE60", NYCZoning::ZoningPalette.color_for("PARK")
  end

  def test_public_area
    assert_equal "27AE60", NYCZoning::ZoningPalette.color_for("PA-1")
  end

  def test_default_unknown
    assert_equal "95A5A6", NYCZoning::ZoningPalette.color_for("UNKNOWN")
  end

  def test_case_insensitive
    assert_equal "4A90D9", NYCZoning::ZoningPalette.color_for("c5-3")
  end
end
