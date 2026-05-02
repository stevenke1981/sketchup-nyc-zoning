module NYCZoning
  # Lightweight cancelable progress wrapper.
  # Sends JS callbacks to an HtmlDialog when provided.
  class Progress
    attr_reader :cancelled

    def initialize(total, dialog: nil)
      @total     = total
      @done      = 0
      @cancelled = false
      @dialog    = dialog
    end

    def increment(n = 1)
      @done += n
      pct = @total > 0 ? (@done * 100 / @total) : 0
      @dialog&.execute_script("onProgress(#{@done}, #{@total}, #{pct})")
    end

    def cancel!
      @cancelled = true
    end

    def complete
      @dialog&.execute_script("onProgress(#{@total}, #{@total}, 100)")
    end
  end
end
