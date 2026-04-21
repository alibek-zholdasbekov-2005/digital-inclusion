import { create } from 'zustand'
import { tokenStore } from '../api/client'
import { getMe, login as apiLogin, logout as apiLogout } from '../api/auth'
import type { User } from '../types'

interface AuthState {
  user: User | null
  loading: boolean
  initialized: boolean
  init: () => Promise<void>
  signIn: (username: string, password: string) => Promise<void>
  signOut: () => void
  setUser: (user: User | null) => void
}

export const useAuth = create<AuthState>((set) => ({
  user: null,
  loading: false,
  initialized: false,

  async init() {
    if (!tokenStore.getAccess()) {
      set({ initialized: true })
      return
    }
    set({ loading: true })
    try {
      const user = await getMe()
      set({ user, loading: false, initialized: true })
    } catch {
      tokenStore.clear()
      set({ user: null, loading: false, initialized: true })
    }
  },

  async signIn(username, password) {
    set({ loading: true })
    try {
      await apiLogin(username, password)
      const user = await getMe()
      set({ user, loading: false })
    } catch (err) {
      set({ loading: false })
      throw err
    }
  },

  signOut() {
    apiLogout()
    set({ user: null })
  },

  setUser(user) {
    set({ user })
  },
}))
