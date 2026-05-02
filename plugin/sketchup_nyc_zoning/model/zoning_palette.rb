module NYCZoning
  module ZoningPalette
    CATEGORY_COLORS = {
      "R"    => "F5DEB3",  # Residential — wheat
      "C"    => "4A90D9",  # Commercial — blue
      "M"    => "C0392B",  # Manufacturing — red-brown
      "PARK" => "27AE60",  # Parks — green
      "PA"   => "27AE60",  # Public area — green
      "BPC"  => "8E44AD",  # Battery Park City — purple
    }.freeze
    DEFAULT_COLOR = "95A5A6".freeze  # gray

    def self.color_for(zoning_district)
      CATEGORY_COLORS.each do |prefix, hex|
        return hex if zoning_district.to_s.upcase.start_with?(prefix)
      end
      DEFAULT_COLOR
    end

    def self.material_for(zoning_district, model)
      hex  = color_for(zoning_district)
      name = "nyc_zone_#{hex}"
      mat  = model.materials[name]
      unless mat
        mat       = model.materials.add(name)
        mat.color = Sketchup::Color.new(
          hex[0, 2].to_i(16),
          hex[2, 2].to_i(16),
          hex[4, 2].to_i(16),
        )
        mat.alpha = 0.85
      end
      mat
    end
  end
end
