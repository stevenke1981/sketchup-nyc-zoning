require "json"
require "sketchup.rb"

module NYCZoning
  module Dialog
    DIALOG_OPTIONS = {
      dialog_title:    "NYC Zoning Loader",
      preferences_key: "nyc_zoning_loader",
      style:           UI::HtmlDialog::STYLE_DIALOG,
      resizable:       true,
      width:           420,
      height:          520,
    }.freeze

    HTML_PATH = File.join(NYCZoning::PLUGIN_DIR, "ui", "dialog.html")

    def self.show
      @dialog ||= build_dialog
      @dialog.show
    end

    def self.build_dialog
      dlg = UI::HtmlDialog.new(DIALOG_OPTIONS)
      dlg.set_file(HTML_PATH)

      dlg.add_action_callback("load_area") do |_ctx, params|
        handle_load(JSON.parse(params))
      end

      dlg.add_action_callback("cancel_load") do |_ctx, _params|
        @loader&.cancel!
      end

      dlg
    end
    private_class_method :build_dialog

    def self.handle_load(params)
      bbox = bbox_from_params(params)
      return unless bbox

      client   = McpClient.new
      raw_text = client.call_tool(
        "query_buildings",
        bbox.to_mcp_params.merge(limit: Config["max_features"] || 10_000),
      )
      geojson  = JSON.parse(raw_text)
      features = geojson["features"] || []

      notify_progress(0, features.length)

      @loader = ChunkLoader.new(features, Sketchup.active_model)
      @loader.run do |done, total|
        notify_progress(done, total)
      end

      @dialog.execute_script(
        "onLoadComplete(#{@loader.loaded}, #{@loader.skipped}, #{@loader.cancelled})",
      )
    rescue StandardError => e
      @dialog.execute_script("onError(#{e.message.to_json})")
      NYCZoning::Logger.error("Dialog load error: #{e.message}")
    end

    def self.bbox_from_params(params)
      mode = params["mode"]
      case mode
      when "borough"
        BoroughIndex.bbox(params["borough"])
      when "zip"
        ZipIndex.bbox(params["zip"])
      when "bbox"
        BBox.new(
          params["min_lon"].to_f, params["min_lat"].to_f,
          params["max_lon"].to_f, params["max_lat"].to_f,
        )
      end
    end
    private_class_method :bbox_from_params

    def self.notify_progress(done, total)
      pct = total > 0 ? (done * 100 / total) : 0
      @dialog.execute_script("onProgress(#{done}, #{total}, #{pct})")
    end
    private_class_method :notify_progress
  end
end
