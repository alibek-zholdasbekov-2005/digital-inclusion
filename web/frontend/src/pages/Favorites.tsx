import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { listFavorites, removeFavorite } from '../api/favorites'
import type { Favorite } from '../types'
import Spinner from '../components/Spinner'

export default function Favorites() {
  const { t } = useTranslation()
  const [items, setItems] = useState<Favorite[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [busyId, setBusyId] = useState<number | null>(null)

  useEffect(() => {
    let cancelled = false
    async function load() {
      setLoading(true)
      try {
        const data = await listFavorites()
        if (!cancelled) setItems(data)
      } catch {
        if (!cancelled) setError(t('favorites.no_favorites'))
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => {
      cancelled = true
    }
  }, [t])

  const onRemove = async (favId: number) => {
    setBusyId(favId)
    try {
      await removeFavorite(favId)
      setItems((prev) => prev.filter((x) => x.id !== favId))
    } finally {
      setBusyId(null)
    }
  }

  if (loading) return <Spinner />

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-slate-900 mb-6">
        {t('favorites.title')} ({items.length})
      </h1>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 text-sm px-3 py-2 rounded mb-4">
          {error}
        </div>
      )}

      {items.length === 0 && !error && (
        <div className="text-center py-12 text-slate-500">
          {t('favorites.no_favorites')}{' '}
          <Link to="/objects" className="text-brand-600 hover:underline">
            {t('favorites.go_to_list')}
          </Link>
        </div>
      )}

      <div className="space-y-2">
        {items.map((f) => (
          <div
            key={f.id}
            className="flex items-center gap-3 bg-white border rounded-lg px-4 py-3"
          >
            <Link
              to={`/objects/${f.object}`}
              className="flex-1 font-medium text-slate-900 hover:text-brand-600"
            >
              {f.object_name || `Объект #${f.object}`}
            </Link>
            <span className="text-xs text-slate-500">
              {new Date(f.created_at).toLocaleDateString('ru-RU')}
            </span>
            <button
              onClick={() => onRemove(f.id)}
              disabled={busyId === f.id}
              className="text-sm text-red-500 hover:text-red-700 disabled:opacity-50"
              aria-label="Убрать"
            >
              ✕
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
