import { api } from './client'
import type {
  AccessibilityObjectDetail,
  AccessibilityObjectSummary,
  BusStop,
} from '../types'

type Paginated<T> = { results?: T[] } | T[]

function unwrap<T>(data: Paginated<T>): T[] {
  if (Array.isArray(data)) return data
  return data.results ?? []
}

export async function listObjects(params?: {
  search?: string
  district?: number
  category?: number
}) {
  const { data } = await api.get('/api/objects/', { params })
  return unwrap<AccessibilityObjectSummary>(data)
}

export async function getObject(id: number | string) {
  const { data } = await api.get(`/api/objects/${id}/`)
  return data as AccessibilityObjectDetail
}

export async function listBusStops() {
  const { data } = await api.get('/api/bus-stops/')
  return unwrap<BusStop>(data)
}

export async function searchObjects(q: string) {
  const { data } = await api.get('/api/search/', { params: { q } })
  return unwrap<AccessibilityObjectSummary>(data)
}

export async function nearbyObjects(lat: number, lon: number, dist = 2000) {
  const { data } = await api.get('/api/objects/nearby/', {
    params: { lat, lon, dist },
  })
  return unwrap<AccessibilityObjectSummary>(data)
}
