// Parse "location" fields coming from the Django backend.
// The backend uses PostGIS PointField which, without rest_framework_gis,
// is serialized as a WKT string like "SRID=4326;POINT (76.88 43.23)".
// If rest_framework_gis is ever added it returns GeoJSON. We support both.

export type LonLat = [number, number]

export type RawLocation =
  | string
  | { type: string; coordinates: LonLat }
  | null
  | undefined

export function parsePoint(loc: RawLocation): LonLat | null {
  if (!loc) return null

  // GeoJSON: { type: 'Point', coordinates: [lon, lat] }
  if (typeof loc === 'object' && Array.isArray(loc.coordinates)) {
    const [lon, lat] = loc.coordinates
    if (typeof lon === 'number' && typeof lat === 'number') {
      return [lon, lat]
    }
    return null
  }

  // WKT: "SRID=4326;POINT (76.88 43.23)" or "POINT (76.88 43.23)"
  if (typeof loc === 'string') {
    const match = loc.match(/POINT\s*\(\s*(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s*\)/i)
    if (match) {
      return [parseFloat(match[1]), parseFloat(match[2])]
    }
  }

  return null
}

/** Leaflet expects [lat, lng], PostGIS gives [lon, lat]. Convert. */
export function toLatLng(p: LonLat): [number, number] {
  return [p[1], p[0]]
}
