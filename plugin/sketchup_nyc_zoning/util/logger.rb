module NYCZoning
  module Logger
    LOG_DIR = File.join(NYCZoning::PLUGIN_DIR, "..", "..", "data", "logs")

    def self.info(msg)  = write("INFO",  msg)
    def self.warn(msg)  = write("WARN",  msg)
    def self.error(msg) = write("ERROR", msg)

    def self.write(level, msg)
      line = "#{Time.now.strftime('%Y-%m-%dT%H:%M:%S')} [#{level}] #{msg}"
      $stdout.puts("[NYCZoning] #{line}")
      append_to_file(line)
    rescue StandardError
      nil
    end

    def self.append_to_file(line)
      Dir.mkdir(LOG_DIR) unless Dir.exist?(LOG_DIR)
      File.open(File.join(LOG_DIR, "plugin.log"), "a") { |f| f.puts(line) }
    end
    private_class_method :append_to_file
  end
end
