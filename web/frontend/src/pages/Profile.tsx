import { FormEvent, useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { updateMe } from '../api/auth'
import { useAuth } from '../store/auth'

export default function Profile() {
  const { t } = useTranslation()
  const { user, setUser } = useAuth()
  const [email, setEmail] = useState(user?.email || '')
  const [busy, setBusy] = useState(false)
  const [msg, setMsg] = useState<string | null>(null)
  const [err, setErr] = useState<string | null>(null)

  useEffect(() => {
    setEmail(user?.email || '')
  }, [user])

  if (!user) return null

  const onSave = async (e: FormEvent) => {
    e.preventDefault()
    setBusy(true)
    setErr(null)
    setMsg(null)
    try {
      const updated = await updateMe({ email })
      setUser(updated)
      setMsg(t('profile.saved'))
    } catch (err: unknown) {
      const detail =
        (err as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail || t('common.error')
      setErr(detail)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="max-w-xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-slate-900 mb-6">{t('profile.title')}</h1>

      <div className="bg-white border rounded-xl p-6 mb-6">
        <div className="flex items-center gap-4 mb-4">
          <div className="w-16 h-16 rounded-full bg-brand-600 text-white flex items-center justify-center text-2xl font-bold">
            {user.username[0]?.toUpperCase()}
          </div>
          <div>
            <div className="font-semibold text-lg">{user.username}</div>
            <div className="text-sm text-slate-500 font-mono">ID: {user.id}</div>
          </div>
        </div>

        <form onSubmit={onSave} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              {t('auth.email')}
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none"
            />
          </div>

          {msg && <div className="text-sm text-green-600">{msg}</div>}
          {err && <div className="text-sm text-red-600">{err}</div>}

          <button
            type="submit"
            disabled={busy}
            className="px-4 py-2 bg-brand-600 hover:bg-brand-700 disabled:opacity-60 text-white rounded transition"
          >
            {busy ? t('auth.creating') : t('common.save', 'Сохранить')}
          </button>
        </form>
      </div>
    </div>
  )
}
