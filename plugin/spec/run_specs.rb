#!/usr/bin/env ruby
# Run all plugin specs outside SketchUp (pure-logic tests only).
# Usage: ruby spec/run_specs.rb
$LOAD_PATH.unshift File.join(__dir__, "..")
require "minitest/autorun"
Dir[File.join(__dir__, "*_spec.rb")].each { |f| require f }
