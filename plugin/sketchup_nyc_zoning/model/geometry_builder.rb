module NYCZoning
  class GeometryBuilder
    METERS_TO_INCHES = 39.3701

    def initialize(model)
      @model = model
    end

    def build_building(feature)
      props = feature["properties"]
      rings = props["rings"]
      return nil if rings.nil? || rings.empty?

      outer_ring = rings[0]
      return nil if outer_ring.length < 3

      height_m  = props["height_m"].to_f
      height_m  = 3.0 if height_m <= 0
      height_in = height_m * METERS_TO_INCHES

      points = ring_to_points(outer_ring)
      return nil if points.length < 3

      group    = @model.active_entities.add_group
      entities = group.entities

      face = entities.add_face(points)
      return nil unless face

      # Ensure face normal points up before extrusion
      face.reverse! if face.normal.z < 0

      face.pushpull(height_in)

      material = ZoningPalette.material_for(
        props["zoning_district"].to_s, @model
      )
      group.entities.each { |e| e.material = material if e.is_a?(Sketchup::Face) }

      AttributeTagger.tag(group, props)
      group
    rescue StandardError => e
      NYCZoning::Logger.warn("GeometryBuilder skip bin=#{feature.dig('properties','bin')}: #{e.message}")
      nil
    end

    private

    def ring_to_points(ring)
      ring.map do |pt|
        Geom::Point3d.new(
          pt[0].to_f * METERS_TO_INCHES,
          pt[1].to_f * METERS_TO_INCHES,
          0,
        )
      end
    end
  end
end
