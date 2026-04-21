import { api, tokenStore } from './client'
import type { User } from '../types'

export async function login(username: string, password: string) {
  const { data } = await api.post('/api/token/', { username, password })
  tokenStore.set(data.access, data.refresh)
  return data as { access: string; refresh: string }
}

export async function register(payload: {
  username: string
  password: string
  email: string
}) {
  const { data } = await api.post('/api/register/', payload)
  return data as User
}

export async function getMe() {
  const { data } = await api.get('/api/me/')
  return data as User
}

export async function updateMe(payload: Partial<User>) {
  const { data } = await api.patch('/api/me/', payload)
  return data as User
}

export function logout() {
  tokenStore.clear()
}
