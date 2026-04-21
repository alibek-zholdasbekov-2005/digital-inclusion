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

export async function createObject(payload: Partial<AccessibilityObjectDetail>) {
  const { data } = await api.post('/api/objects/', payload)
  return data as AccessibilityObjectDetail
}

export async function updateObject(
  id: number | string,
  payload: Partial<AccessibilityObjectDetail>,
) {
  const { data } = await api.patch(`/api/objects/${id}/`, payload)
  return data as AccessibilityObjectDetail
}

export async function submitObject(id: number | string) {
  const { data } = await api.post(`/api/objects/${id}/submit/`)
  return data as AccessibilityObjectDetail
}

export async function uploadObjectPhoto(id: number | string, file: File) {
  const form = new FormData()
  form.append('image', file)
  const { data } = await api.post(`/api/objects/${id}/photos/`, form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data as { id: number; image: string }
}
