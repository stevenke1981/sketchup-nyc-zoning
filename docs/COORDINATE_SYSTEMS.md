# Coordinate Systems

## Pipeline Transform Chain

```
NYC Open Data (EPSG:4326 WGS84 lon/lat)
    ↓  pyproj: 4326 → 2263 (NY State Plane, US survey feet)
EPSG:2263
    ↓  subtract anchor in 2263, convert feet → meters (× 0.3048006096)
local_x_m, local_y_m  (origin = bbox anchor point)
    ↓  wire format to Ruby plugin
SketchUp Geom::Point3d (meters)
```

## Anchor Point

- **Definition**: Center of the user-requested bbox
- **Purpose**: Keeps all coordinates near origin; avoids SketchUp 32-bit precision loss at absolute NY State Plane values (millions of feet)
- **Limit**: Accurate to < 5 cm within ~3 km radius of anchor (sufficient for massing)

## Height

- Primary field: `heightroof` (feet, from NYC building footprints)
- Fallback 1: `numfloors × 3.5 m`
- Fallback 2: `3.0 m` placeholder
- Metadata field `height_source` records which was used

## Wire Format (GeoJSON properties per feature)

```json
{
  "bbl": "1008880001",
  "zoning_district": "C5-3",
  "height_ft": 1454.0,
  "height_m": 443.1,
  "height_source": "heightroof",
  "year_built": 1931,
  "land_use": "05",
  "rings": [
    [[local_x_m, local_y_m], ...],  // outer ring
    [[local_x_m, local_y_m], ...]   // inner rings (holes)
  ],
  "color_hex": "#4A90D9",
  "anchor_lat": 40.7484,
  "anchor_lon": -73.9856
}
```
