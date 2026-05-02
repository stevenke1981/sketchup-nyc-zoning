require "sketchup.rb"

module NYCZoning
  PLUGIN_DIR = File.dirname(__FILE__)

  autoload :Config,          File.join(PLUGIN_DIR, "util", "config")
  autoload :Logger,          File.join(PLUGIN_DIR, "util", "logger")
  autoload :HttpClient,      File.join(PLUGIN_DIR, "net", "http_client")
  autoload :McpClient,       File.join(PLUGIN_DIR, "net", "mcp_client")
  autoload :BBox,            File.join(PLUGIN_DIR, "geo", "bbox")
  autoload :CoordConverter,  File.join(PLUGIN_DIR, "geo", "coord_converter")
  autoload :BoroughIndex,    File.join(PLUGIN_DIR, "geo", "borough_index")
  autoload :ZipIndex,        File.join(PLUGIN_DIR, "geo", "zip_index")
  autoload :GeometryBuilder, File.join(PLUGIN_DIR, "model", "geometry_builder")
  autoload :AttributeTagger, File.join(PLUGIN_DIR, "model", "attribute_tagger")
  autoload :ZoningPalette,   File.join(PLUGIN_DIR, "model", "zoning_palette")
  autoload :ChunkLoader,     File.join(PLUGIN_DIR, "model", "chunk_loader")
  autoload :Dialog,          File.join(PLUGIN_DIR, "ui", "dialog")

  unless file_loaded?(__FILE__)
    menu = UI.menu("Plugins")
    menu.add_item("NYC Zoning - Load Model") { Dialog.show }
    file_loaded(__FILE__)
  end
end
