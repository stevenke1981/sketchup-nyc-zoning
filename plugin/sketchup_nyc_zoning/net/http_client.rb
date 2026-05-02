require "net/http"
require "uri"

module NYCZoning
  class HttpClient
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds

    def initialize(timeout: 30)
      @timeout = timeout
    end

    def get(url, params = {})
      uri = URI.parse(url)
      uri.query = URI.encode_www_form(params) unless params.empty?

      retries = 0
      begin
        http          = Net::HTTP.new(uri.host, uri.port)
        http.use_ssl  = uri.scheme == "https"
        http.open_timeout = @timeout
        http.read_timeout = @timeout

        req = Net::HTTP::Get.new(uri.request_uri)
        req["Accept"] = "application/json"
        resp = http.request(req)
        raise "HTTP #{resp.code}" unless resp.is_a?(Net::HTTPSuccess)
        resp.body
      rescue StandardError => e
        retries += 1
        if retries <= MAX_RETRIES
          sleep(RETRY_DELAY * retries)
          retry
        end
        raise
      end
    end
  end
end
