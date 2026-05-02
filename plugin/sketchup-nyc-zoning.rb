# SketchUp NYC Zoning Plugin — loader stub
require "sketchup.rb"
require "extensions.rb"

module NYCZoning
  PLUGIN_ID      = "sketchup-nyc-zoning".freeze
  PLUGIN_NAME    = "NYC Zoning".freeze
  PLUGIN_VERSION = "0.1.0".freeze

  loader = File.join(__dir__, "sketchup_nyc_zoning", "main")

  extension = SketchupExtension.new(PLUGIN_NAME, loader)
  extension.description = "Load real NYC zoning 3D models from NYC Open Data."
  extension.version     = PLUGIN_VERSION
  extension.creator     = "nyc-zoning contributors"

  Sketchup.register_extension(extension, true)
end
