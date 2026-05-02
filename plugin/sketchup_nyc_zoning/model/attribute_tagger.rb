module NYCZoning
  module AttributeTagger
    DICT = "nyc_zoning".freeze
    FIELDS = %w[bbl bin address zoning_district zoning_category
                height_ft height_m height_source numfloors
                year_built land_use color_hex anchor_lon anchor_lat].freeze

    def self.tag(group, props)
      FIELDS.each do |field|
        v = props[field]
        group.set_attribute(DICT, field, v) unless v.nil?
      end
    end
  end
end
