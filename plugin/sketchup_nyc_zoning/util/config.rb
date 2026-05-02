require "json"

module NYCZoning
  module Config
    CONFIG_PATH = File.join(NYCZoning::PLUGIN_DIR, "..", "config", "config.json")
    DEFAULTS = {
      "mcp_url"      => "http://127.0.0.1:8765",
      "bearer_token" => "",
      "chunk_size"   => 250,
      "max_features" => 10_000,
    }.freeze

    def self.load
      return DEFAULTS unless File.exist?(CONFIG_PATH)
      DEFAULTS.merge(JSON.parse(File.read(CONFIG_PATH)))
    rescue JSON::ParserError
      DEFAULTS
    end

    def self.[](key)
      @data ||= load
      @data[key.to_s]
    end
  end
end
