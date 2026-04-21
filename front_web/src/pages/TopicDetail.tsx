import { FormEvent, useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { createPost, getTopic, listPosts } from '../api/forum'
import type { ForumPost, ForumTopic } from '../types'
import { useAuth } from '../store/auth'
import Spinner from '../components/Spinner'

function authorName(p: ForumPost | ForumTopic): string {
  return p.author_name || `user #${p.author}`
}

export default function TopicDetail() {
  const { id } = useParams<{ id: string }>()
  const { user } = useAuth()

  const [topic, setTopic] = useState<ForumTopic | null>(null)
  const [posts, setPosts] = useState<ForumPost[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [text, setText] = useState('')
  const [image, setImage] = useState<File | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const [submitErr, setSubmitErr] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return
    let cancelled = false
    async function load() {
      setLoading(true)
      try {
        const [t, p] = await Promise.all([
          getTopic(id!),
          listPosts(id!).catch(() => []),
        ])
        if (!cancelled) {
          setTopic(t)
          setPosts(p)
        }
      } catch {
        if (!cancelled) setError('Тема не найдена')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => {
      cancelled = true
    }
  }, [id])

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!id || !text.trim()) return
    setSubmitting(true)
    setSubmitErr(null)
    try {
      const post = await createPost(Number(id), text.trim(), image)
      setPosts((prev) => [...prev, post])
      setText('')
      setImage(null)
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail || 'Не удалось отправить сообщение'
      setSubmitErr(msg)
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <Spinner />

  if (error || !topic) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-12 text-center">
        <p className="text-slate-600">{error || 'Тема не найдена'}</p>
        <Link to="/forum" className="text-brand-600 hover:underline mt-4 inline-block">
          ← К списку тем
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <Link to="/forum" className="text-sm text-slate-500 hover:text-brand-600">
        ← К форуму
      </Link>

      <h1 className="text-2xl font-bold text-slate-900 mt-4 mb-1">
        {topic.title}
      </h1>
      <p className="text-sm text-slate-500 mb-6">
        Создано: {new Date(topic.created_at).toLocaleString('ru-RU')}
      </p>

      <div className="space-y-3 mb-6">
        {posts.map((p) => (
          <div key={p.id} className="bg-white border rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-slate-900">
                {authorName(p)}
              </span>
              <span className="text-xs text-slate-500">
                {new Date(p.created_at).toLocaleString('ru-RU')}
              </span>
            </div>
            <p className="text-sm text-slate-800 whitespace-pre-line">{p.text}</p>
            {p.image && (
              <img
                src={p.image}
                alt=""
                className="mt-3 max-h-64 rounded border"
                loading="lazy"
              />
            )}
          </div>
        ))}
        {posts.length === 0 && (
          <p className="text-sm text-slate-500 text-center py-6">
            Пока нет сообщений
          </p>
        )}
      </div>

      {user ? (
        <form
          onSubmit={onSubmit}
          className="bg-white border rounded-xl p-5 space-y-3"
        >
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Ваше сообщение..."
            rows={3}
            required
            className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none"
          />
          <div className="flex items-center gap-3">
            <label className="inline-flex items-center gap-2 text-sm text-slate-600 cursor-pointer">
              <span className="px-3 py-1.5 border rounded-md hover:bg-slate-50">
                {image ? '📎 Заменить' : '📎 Прикрепить фото'}
              </span>
              <input
                type="file"
                accept="image/*"
                onChange={(e) => setImage(e.target.files?.[0] || null)}
                className="hidden"
              />
            </label>
            {image && (
              <>
                <span className="text-xs text-slate-500 truncate max-w-[200px]">
                  {image.name}
                </span>
                <button
                  type="button"
                  onClick={() => setImage(null)}
                  className="text-xs text-red-500 hover:underline"
                >
                  удалить
                </button>
              </>
            )}
          </div>
          {submitErr && <div className="text-sm text-red-600">{submitErr}</div>}
          <button
            type="submit"
            disabled={submitting || !text.trim()}
            className="px-4 py-2 bg-brand-600 hover:bg-brand-700 disabled:opacity-60 text-white rounded transition"
          >
            {submitting ? 'Отправка...' : 'Отправить'}
          </button>
        </form>
      ) : (
        <div className="bg-slate-50 border rounded-xl p-4 text-sm text-slate-600">
          <Link to="/login" className="text-brand-600 hover:underline">
            Войдите
          </Link>
          , чтобы оставить сообщение
        </div>
      )}
    </div>
  )
}
