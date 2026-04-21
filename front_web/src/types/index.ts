// Types mirroring Django REST API

export interface User {
  id: number
  username: string
  email: string
}

export interface Tokens {
  access: string
  refresh: string
}

// location may come as GeoJSON object OR as WKT string depending on backend config
export type RawGeoLocation =
  | { type: 'Point'; coordinates: [number, number] }
  | string
  | null

export interface AccessibilityObjectSummary {
  id: number
  name_ru: string | null
  district: number | null
  district_name?: string | null
  category: number | null
  category_info?: { id: number; name_ru: string; icon?: string; color?: string } | null
  location: RawGeoLocation
  accessibility_summary?: string
  avg_rating?: number | null
  reviews_count?: number
}

export interface AccessibilityObjectDetail extends AccessibilityObjectSummary {
  full_legal_name: string | null
  activity_type: number | null
  ownership_type: number | null
  responsible_body: number | null
  territory?: {
    entrance_width_ok: boolean
    parking_has_disabled_spots: boolean
  }
  entrance_group?: {
    has_ramp: boolean
    has_braille: boolean
    has_call_button: boolean
    has_visual_info: boolean
  }
  movement_ways?: {
    width_ok: boolean
    has_handrails: boolean
    tactile_indicators: boolean
  }
  service_zones?: { counter_height_ok: boolean }
  sanitary_rooms?: { toilet_accessible: boolean }
  info_telecom?: {
    has_audio_guide: boolean
    induction_loop: boolean
    has_visual_info: boolean
  }
  photos?: { id: number; image: string }[]
  reviews?: Review[]
}

export interface BusStop {
  id: number
  stop_name: string | null
  district: number | null
  comment: string | null
  location: RawGeoLocation
  total_status?: string
}

export interface ForumTopic {
  id: number
  title: string
  author: number
  author_name?: string
  created_at: string
  is_archived: boolean
  posts_count?: number
}

export interface ForumPost {
  id: number
  topic: number
  author: number
  author_name?: string
  text: string
  image: string | null
  created_at: string
}

export interface Review {
  id: number
  object: number
  author: number
  author_name?: string
  rating: number
  text: string
  photo: string | null
  created_at: string
}

export interface District {
  id: number
  name_ru: string | null
  name_kz: string | null
}

export interface Category {
  id: number
  name_ru: string
  name_kz?: string
  icon?: string | null
  color?: string
  sort_order?: number
}

export interface Favorite {
  id: number
  object: number
  object_name?: string | null
  created_at: string
}
