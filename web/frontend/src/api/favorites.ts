import { api } from './client'
import type { Favorite } from '../types'

type Paginated<T> = { results?: T[] } | T[]

function unwrap<T>(data: Paginated<T>): T[] {
  if (Array.isArray(data)) return data
  return data.results ?? []
}

export async function listFavorites() {
  const { data } = await api.get('/api/favorites/')
  return unwrap<Favorite>(data)
}

export async function addFavorite(objectId: number) {
  const { data } = await api.post('/api/favorites/', { object: objectId })
  return data as Favorite
}

export async function removeFavorite(favoriteId: number) {
  await api.delete(`/api/favorites/${favoriteId}/`)
}

/** Helper: check if object is favorited by current user. Returns favorite id or null. */
export async function findFavorite(objectId: number): Promise<Favorite | null> {
  try {
    const { data } = await api.get('/api/favorites/', {
      params: { object: objectId },
    })
    const list = unwrap<Favorite>(data)
    return list.find((f) => f.object === objectId) ?? null
  } catch {
    return null
  }
}
