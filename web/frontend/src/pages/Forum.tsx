import { FormEvent, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { createTopic, listTopics } from '../api/forum'
import type { ForumTopic } from '../types'
import { useAuth } from '../store/auth'
import Spinner from '../components/Spinner'

export default function Forum() {
  const { user } = useAuth()
  const [topics, setTopics] = useState<ForumTopic[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [query, setQuery] = useState('')

  const [newTitle, setNewTitle] = useState('')
  const [creating, setCreating] = useState(false)
  const [createErr, setCreateErr] = useState<string | null>(null)
  const [showForm, setShowForm] = useState(false)

  useEffect(() => {
    load('')
  }, [])

  async function load(search: string) {
    setLoading(true)
    try {
      const data = await listTopics(search || undefined)
      setTopics(data)
    } catch {
      setError('Не удалось загрузить темы')
    } finally {
      setLoading(false)
    }
  }

  const onSearch = (e: FormEvent) => {
    e.preventDefault()
    load(query.trim())
  }

  const onCreate = async (e: FormEvent) => {
    e.preventDefault()
    if (!newTitle.trim()) return
    setCreating(true)
    setCreateErr(null)
    try {
      const topic = await createTopic(newTitle.trim())
      setTopics((prev) => [topic, ...prev])
      setNewTitle('')
      setShowForm(false)
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail || 'Не удалось создать тему'
      setCreateErr(msg)
    } finally {
      setCreating(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Форум</h1>
        {user && (
          <button
            onClick={() => setShowForm((v) => !v)}
            className="px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-md transition"
          >
            {showForm ? 'Отмена' : '+ Новая тема'}
          </button>
        )}
      </div>

      {showForm && user && (
        <form
          onSubmit={onCreate}
          className="bg-white border rounded-xl p-5 mb-6 space-y-3"
        >
          <input
            type="text"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            placeholder="Название темы"
            required
            autoFocus
            className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none"
          />
          {createErr && <div className="text-sm text-red-600">{createErr}</div>}
          <button
            type="submit"
            disabled={creating || !newTitle.trim()}
            className="px-4 py-2 bg-brand-600 hover:bg-brand-700 disabled:opacity-60 text-white rounded transition"
          >
            {creating ? 'Создаём...' : 'Создать тему'}
          </button>
        </form>
      )}

      <form onSubmit={onSearch} className="flex gap-2 mb-4">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Поиск по темам..."
          className="flex-1 px-3 py-2 border rounded-md focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none"
        />
        <button
          type="submit"
          className="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-800 rounded-md transition"
        >
          Найти
        </button>
      </form>

      {loading && <Spinner />}

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 text-sm px-3 py-2 rounded mb-4">
          {error}
        </div>
      )}

      {!loading && (
        <div className="space-y-2">
          {topics.map((t) => (
            <Link
              key={t.id}
              to={`/forum/${t.id}`}
              className="block bg-white border rounded-lg px-4 py-3 hover:shadow-md hover:border-brand-300 transition"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="font-medium text-slate-900">{t.title}</div>
                  <div className="text-xs text-slate-500 mt-1">
                    {t.author_name && <span>{t.author_name} · </span>}
                    {new Date(t.created_at).toLocaleString('ru-RU')}
                  </div>
                </div>
                {typeof t.posts_count === 'number' && (
                  <span className="shrink-0 inline-flex items-center justify-center min-w-[2rem] h-7 px-2 rounded-full bg-brand-50 text-brand-700 text-xs font-medium">
                    {t.posts_count}
                  </span>
                )}
              </div>
            </Link>
          ))}
          {topics.length === 0 && (
            <div className="text-center py-12 text-slate-500">
              Пока нет тем. {user && 'Создайте первую!'}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
