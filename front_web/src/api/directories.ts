import { api } from './client'
import type { District, Category } from '../types'

type Paginated<T> = { results?: T[] } | T[]

function unwrap<T>(data: Paginated<T>): T[] {
  if (Array.isArray(data)) return data
  return data.results ?? []
}

export async function listDistricts() {
  const { data } = await api.get('/api/districts/')
  return unwrap<District>(data)
}

export async function listCategories() {
  const { data } = await api.get('/api/categories/')
  return unwrap<Category>(data)
}
