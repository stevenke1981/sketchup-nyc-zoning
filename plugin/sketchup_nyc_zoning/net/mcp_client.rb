require "net/http"
require "uri"
require "json"

module NYCZoning
  class McpClient
    def initialize(base_url: Config["mcp_url"], token: Config["bearer_token"])
      @uri   = URI.parse(base_url)
      @token = token
      @seq   = 0
    end

    def call_tool(name, arguments = {})
      @seq += 1
      body = {
        jsonrpc: "2.0",
        id:      @seq,
        method:  "tools/call",
        params:  { name: name, arguments: arguments },
      }.to_json

      http = Net::HTTP.new(@uri.host, @uri.port)
      http.open_timeout = 10
      http.read_timeout = 60

      req = Net::HTTP::Post.new(@uri.path.empty? ? "/" : @uri.path)
      req["Content-Type"] = "application/json"
      req["Authorization"] = "Bearer #{@token}" unless @token.empty?
      req.body = body

      resp = http.request(req)
      raise "MCP HTTP #{resp.code}" unless resp.is_a?(Net::HTTPSuccess)

      data = JSON.parse(resp.body)
      raise "MCP error: #{data["error"]}" if data["error"]
      data.dig("result", "content", 0, "text")
    end
  end
end
