import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios'

const BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '') ||
  'https://backend-inclusion.onrender.com'

export const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

// ---- Token storage (localStorage) ----
const ACCESS_KEY = 'di_access'
const REFRESH_KEY = 'di_refresh'

export const tokenStore = {
  getAccess: () => localStorage.getItem(ACCESS_KEY),
  getRefresh: () => localStorage.getItem(REFRESH_KEY),
  set: (access: string, refresh: string) => {
    localStorage.setItem(ACCESS_KEY, access)
    localStorage.setItem(REFRESH_KEY, refresh)
  },
  setAccess: (access: string) => localStorage.setItem(ACCESS_KEY, access),
  clear: () => {
    localStorage.removeItem(ACCESS_KEY)
    localStorage.removeItem(REFRESH_KEY)
  },
}

// ---- Request interceptor: attach JWT ----
api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = tokenStore.getAccess()
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// ---- Response interceptor: refresh on 401 ----
let isRefreshing = false
let refreshQueue: ((token: string | null) => void)[] = []

const processQueue = (token: string | null) => {
  refreshQueue.forEach((cb) => cb(token))
  refreshQueue = []
}

api.interceptors.response.use(
  (resp) => resp,
  async (error: AxiosError) => {
    const original = error.config as InternalAxiosRequestConfig & {
      _retry?: boolean
    }

    if (
      error.response?.status === 401 &&
      !original?._retry &&
      !original?.url?.includes('/api/token/')
    ) {
      const refresh = tokenStore.getRefresh()
      if (!refresh) {
        tokenStore.clear()
        return Promise.reject(error)
      }

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          refreshQueue.push((token) => {
            if (token && original.headers) {
              original.headers.Authorization = `Bearer ${token}`
              resolve(api(original))
            } else {
              reject(error)
            }
          })
        })
      }

      original._retry = true
      isRefreshing = true

      try {
        const { data } = await axios.post(`${BASE_URL}/api/token/refresh/`, {
          refresh,
        })
        tokenStore.setAccess(data.access)
        processQueue(data.access)
        if (original.headers) {
          original.headers.Authorization = `Bearer ${data.access}`
        }
        return api(original)
      } catch (err) {
        processQueue(null)
        tokenStore.clear()
        window.location.href = '/login'
        return Promise.reject(err)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  },
)
