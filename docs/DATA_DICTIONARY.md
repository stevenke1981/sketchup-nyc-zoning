# Data Dictionary

## Unified Schema (internal model)

| Field | Type | Source | Notes |
|-------|------|--------|-------|
| `bbl` | str | PLUTO / footprints | Borough-Block-Lot (10 digits) |
| `bin` | str | Footprints | Building Identification Number |
| `address` | str | PLUTO | House number + street |
| `zipcode` | str | PLUTO | 5-digit ZIP |
| `borough` | str | PLUTO | MN/BX/BK/QN/SI |
| `zoning_district` | str | Zoning layer (spatial join) | e.g. R8A, C5-3, M1-5 |
| `zoning_category` | str | Derived | R / C / M / PA / PARK |
| `height_ft` | float | Footprints `heightroof` | Roof height in feet |
| `height_m` | float | Derived | `height_ft × 0.3048` |
| `height_source` | str | Derived | heightroof / numfloors / placeholder |
| `numfloors` | int | Footprints / PLUTO | Floor count |
| `year_built` | int | PLUTO `yearbuilt` | Construction year |
| `land_use` | str | PLUTO `landuse` | 2-digit code (01–11) |
| `far` | float | PLUTO `builtfar` | Floor Area Ratio as-built |
| `lot_area_sqft` | float | PLUTO `lotarea` | Lot area sq ft |
| `bldg_area_sqft` | float | PLUTO `bldgarea` | Gross building area sq ft |
| `footprint_geom` | GeoJSON | Footprints `the_geom` | MultiPolygon WGS84 |

## Source Datasets

### Building Footprints (qrmh-6wdr)
| Socrata column | Maps to | Unit |
|----------------|---------|------|
| `the_geom` | `footprint_geom` | GeoJSON MultiPolygon, WGS84 |
| `heightroof` | `height_ft` | feet |
| `groundelev` | ground elevation | feet |
| `numfloors` | `numfloors` | count |
| `bin` | `bin` | string |
| `doitt_id` | internal | string |
| `lstmoddate` | last modified | ISO date |

### MapPLUTO (64uk-42ks)
| Socrata column | Maps to | Unit |
|----------------|---------|------|
| `bbl` | `bbl` | string |
| `address` | `address` | string |
| `zipcode` | `zipcode` | string |
| `borough` | `borough` | string |
| `yearbuilt` | `year_built` | year |
| `numfloors` | `numfloors` | count |
| `landuse` | `land_use` | 2-digit code |
| `builtfar` | `far` | ratio |
| `lotarea` | `lot_area_sqft` | sq ft |
| `bldgarea` | `bldg_area_sqft` | sq ft |

### Zoning Districts (6tn7-vhp3)
| Socrata column | Maps to | Unit |
|----------------|---------|------|
| `zonedist` | `zoning_district` | string (e.g. R8A) |
| `the_geom` | district polygon | GeoJSON MultiPolygon |
| `label` | display label | string |

## Zoning Category Mapping

| Prefix | Category | Color |
|--------|----------|-------|
| R | Residential | `#F5DEB3` (wheat) |
| C | Commercial | `#4A90D9` (blue) |
| M | Manufacturing | `#C0392B` (red-brown) |
| PARK | Parks | `#27AE60` (green) |
| PA | Public | `#27AE60` (green) |
| BPC | Battery Park City | `#8E44AD` (purple) |
| other | Special / Mixed | `#95A5A6` (gray) |
