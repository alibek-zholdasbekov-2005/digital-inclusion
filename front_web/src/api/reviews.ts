import { api } from './client'
import type { Review } from '../types'

type Paginated<T> = { results?: T[] } | T[]

function unwrap<T>(data: Paginated<T>): T[] {
  if (Array.isArray(data)) return data
  return data.results ?? []
}

export async function listReviews(objectId?: number | string) {
  const { data } = await api.get('/api/reviews/', {
    params: objectId ? { object: objectId } : undefined,
  })
  return unwrap<Review>(data)
}

export async function createReview(payload: {
  object: number
  rating: number
  text: string
  photo?: File | null
}) {
  if (payload.photo) {
    const fd = new FormData()
    fd.append('object', String(payload.object))
    fd.append('rating', String(payload.rating))
    fd.append('text', payload.text)
    fd.append('photo', payload.photo)
    const { data } = await api.post('/api/reviews/', fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return data as Review
  }
  const { data } = await api.post('/api/reviews/', {
    object: payload.object,
    rating: payload.rating,
    text: payload.text,
  })
  return data as Review
}
