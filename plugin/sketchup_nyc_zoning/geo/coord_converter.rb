# Pure Ruby coordinate helpers (no native gems required).
# The pipeline emits local_x_m / local_y_m, so this module handles
# the conversion from SketchUp's inch-based units.
module NYCZoning
  module CoordConverter
    METERS_TO_INCHES = 39.3701
    INCHES_TO_METERS = 1.0 / METERS_TO_INCHES

    # Convert anchor-relative meters to SketchUp Geom::Point3d (inches, z=0)
    def self.meters_to_point(x_m, y_m)
      Geom::Point3d.new(x_m * METERS_TO_INCHES, y_m * METERS_TO_INCHES, 0)
    end

    # Convert a ring of [x_m, y_m] pairs to an array of Geom::Point3d
    def self.ring_to_points(ring)
      ring.map { |pt| meters_to_point(pt[0].to_f, pt[1].to_f) }
    end

    # Height in meters → SketchUp inches
    def self.height_to_inches(height_m)
      height_m.to_f * METERS_TO_INCHES
    end
  end
end
