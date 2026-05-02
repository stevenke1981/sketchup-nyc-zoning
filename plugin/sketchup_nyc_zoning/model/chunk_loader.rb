require "json"

module NYCZoning
  class ChunkLoader
    attr_reader :loaded, :skipped, :cancelled

    def initialize(features, model, chunk_size: Config["chunk_size"] || 250)
      @features   = features
      @model      = model
      @chunk_size = chunk_size.to_i
      @builder    = GeometryBuilder.new(model)
      @loaded     = 0
      @skipped    = 0
      @cancelled  = false
    end

    def run(&progress_cb)
      @features.each_slice(@chunk_size).with_index do |chunk, idx|
        break if @cancelled

        @model.start_operation("NYC Zoning chunk #{idx + 1}", true)
        chunk.each do |feature|
          result = @builder.build_building(feature)
          result ? @loaded += 1 : @skipped += 1
        end
        @model.commit_operation

        progress_cb&.call(@loaded, @features.length)

        # Yield to the SketchUp UI thread between batches
        UI.start_timer(0, false) {} if defined?(UI)
      end
      self
    end

    def cancel!
      @cancelled = true
    end
  end
end
