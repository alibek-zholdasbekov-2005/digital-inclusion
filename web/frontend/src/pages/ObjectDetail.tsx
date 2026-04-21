import { FormEvent, useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { getObject } from '../api/objects'
import { createReview, listReviews } from '../api/reviews'
import { addFavorite, findFavorite, removeFavorite } from '../api/favorites'
import type {
  AccessibilityObjectDetail,
  Favorite,
  Review,
} from '../types'
import { useAuth } from '../store/auth'
import Spinner from '../components/Spinner'

interface Feature {
  label: string
  value: boolean
}

function FeatureList({ title, features }: { title: string; features: Feature[] }) {
  if (features.length === 0) return null
  return (
    <div>
      <h3 className="font-semibold text-slate-900 mb-2">{title}</h3>
      <ul className="space-y-1 text-sm">
        {features.map((f) => (
          <li key={f.label} className="flex items-center gap-2">
            <span
              className={`inline-flex w-5 h-5 rounded-full items-center justify-center text-xs ${
                f.value
                  ? 'bg-green-100 text-green-700'
                  : 'bg-slate-100 text-slate-400'
              }`}
            >
              {f.value ? '✓' : '−'}
            </span>
            <span className={f.value ? 'text-slate-800' : 'text-slate-500'}>
              {f.label}
            </span>
          </li>
        ))}
      </ul>
    </div>
  )
}

function Stars({ value, onChange }: { value: number; onChange?: (n: number) => void }) {
  return (
    <div className="flex gap-1">
      {[1, 2, 3, 4, 5].map((n) => (
        <button
          key={n}
          type="button"
          disabled={!onChange}
          onClick={() => onChange?.(n)}
          className={`text-2xl transition ${
            n <= value ? 'text-yellow-400' : 'text-slate-300'
          } ${onChange ? 'hover:scale-110 cursor-pointer' : 'cursor-default'}`}
          aria-label={`${n} stars`}
        >
          ★
        </button>
      ))}
    </div>
  )
}

export default function ObjectDetail() {
  const { id } = useParams<{ id: string }>()
  const { user } = useAuth()
  const { t, i18n } = useTranslation()
  const [obj, setObj] = useState<AccessibilityObjectDetail | null>(null)
  const [reviews, setReviews] = useState<Review[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [favorite, setFavorite] = useState<Favorite | null>(null)
  const [favBusy, setFavBusy] = useState(false)

  const [rating, setRating] = useState(5)
  const [text, setText] = useState('')
  const [photo, setPhoto] = useState<File | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const [submitErr, setSubmitErr] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return
    let cancelled = false
    async function load() {
      setLoading(true)
      setError(null)
      try {
        const [o, r] = await Promise.all([
          getObject(id!),
          listReviews(id!).catch(() => []),
        ])
        if (!cancelled) {
          setObj(o)
          setReviews(r)
        }
      } catch {
        if (!cancelled) setError(t('common.error'))
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => {
      cancelled = true
    }
  }, [id, t])

  // Check favorite status when user + id are known
  useEffect(() => {
    if (!id || !user) {
      setFavorite(null)
      return
    }
    findFavorite(Number(id)).then(setFavorite).catch(() => setFavorite(null))
  }, [id, user])

  const toggleFavorite = async () => {
    if (!id || !user) return
    setFavBusy(true)
    try {
      if (favorite) {
        await removeFavorite(favorite.id)
        setFavorite(null)
      } else {
        const fav = await addFavorite(Number(id))
        setFavorite(fav)
      }
    } catch {
      // silent
    } finally {
      setFavBusy(false)
    }
  }

  const submitReview = async (e: FormEvent) => {
    e.preventDefault()
    if (!id || !text.trim()) return
    setSubmitting(true)
    setSubmitErr(null)
    try {
      const review = await createReview({
        object: Number(id),
        rating,
        text: text.trim(),
        photo,
      })
      setReviews((prev) => [review, ...prev])
      setText('')
      setRating(5)
      setPhoto(null)
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail || t('common.error')
      setSubmitErr(msg)
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <Spinner />

  if (error || !obj) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 text-center">
        <p className="text-slate-600">{error || t('common.error')}</p>
        <Link to="/objects" className="text-brand-600 hover:underline mt-4 inline-block">
          ← {t('nav.objects')}
        </Link>
      </div>
    )
  }

  const entrance = obj.entrance_group
  const movement = obj.movement_ways
  const territory = obj.territory
  const info = obj.info_telecom
  const sanitary = obj.sanitary_rooms
  const service = obj.service_zones
  const avg = (obj as AccessibilityObjectDetail & { avg_rating?: number | null })
    .avg_rating
  const reviewsCount = (obj as AccessibilityObjectDetail & {
    reviews_count?: number
  }).reviews_count

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <Link to="/objects" className="text-sm text-slate-500 hover:text-brand-600">
        ← {t('nav.objects')}
      </Link>

      <div className="flex items-start justify-between gap-4 mt-4 mb-2">
        <h1 className="text-3xl font-bold text-slate-900">
          {obj.name_ru || 'Объект без названия'}
        </h1>
        {user && (
          <button
            onClick={toggleFavorite}
            disabled={favBusy}
            aria-label="Toggle Favorite"
            className={`shrink-0 w-11 h-11 rounded-full border flex items-center justify-center text-xl transition ${
              favorite
                ? 'bg-red-50 border-red-300 text-red-500'
                : 'bg-white border-slate-300 text-slate-400 hover:text-red-500 hover:border-red-300'
            } ${favBusy ? 'opacity-60' : ''}`}
          >
            {favorite ? '♥' : '♡'}
          </button>
        )}
      </div>

      <div className="flex flex-wrap items-center gap-2 mb-4">
        {obj.category_info && (
          <span
            className="text-xs px-2 py-0.5 rounded-full"
            style={{
              backgroundColor: `${obj.category_info.color || '#2196F3'}20`,
              color: obj.category_info.color || '#2196F3',
            }}
          >
            {obj.category_info.name_ru}
          </span>
        )}
        {obj.district_name && (
          <span className="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
            {obj.district_name}
          </span>
        )}
        {typeof avg === 'number' && (
          <span className="text-xs px-2 py-0.5 rounded-full bg-yellow-50 text-yellow-700">
            ★ {avg.toFixed(1)}
            {reviewsCount ? ` · ${reviewsCount} ` : ''}
          </span>
        )}
      </div>

      {obj.full_legal_name && (
        <p className="text-sm text-slate-600 mb-6">{obj.full_legal_name}</p>
      )}

      {obj.photos && obj.photos.length > 0 && (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mb-6">
          {obj.photos.slice(0, 6).map((p) => (
            <img
              key={p.id}
              src={p.image}
              alt=""
              className="w-full h-32 object-cover rounded-lg border"
              loading="lazy"
            />
          ))}
        </div>
      )}

      <div className="grid md:grid-cols-2 gap-6 bg-white border rounded-xl p-6 mb-8">
        {entrance && (
          <FeatureList
            title="Вход"
            features={[
              { label: 'Пандус', value: entrance.has_ramp },
              { label: 'Шрифт Брайля', value: entrance.has_braille },
              { label: 'Кнопка вызова', value: entrance.has_call_button },
              { label: 'Визуальная информация', value: entrance.has_visual_info },
            ]}
          />
        )}
        {movement && (
          <FeatureList
            title="Пути движения"
            features={[
              { label: 'Ширина путей в норме', value: movement.width_ok },
              { label: 'Поручни', value: movement.has_handrails },
              { label: 'Тактильные указатели', value: movement.tactile_indicators },
            ]}
          />
        )}
        {territory && (
          <FeatureList
            title="Территория"
            features={[
              { label: 'Ширина прохода > 90 см', value: territory.entrance_width_ok },
              {
                label: 'Парковка для МГН',
                value: territory.parking_has_disabled_spots,
              },
            ]}
          />
        )}
        {info && (
          <FeatureList
            title="Информация и связь"
            features={[
              { label: 'Аудиогид', value: info.has_audio_guide },
              { label: 'Индукционная петля', value: info.induction_loop },
              { label: 'Электронное табло', value: info.has_visual_info },
            ]}
          />
        )}
        {sanitary && (
          <FeatureList
            title="Санитарные комнаты"
            features={[
              { label: 'Спец. туалет доступен', value: sanitary.toilet_accessible },
            ]}
          />
        )}
        {service && (
          <FeatureList
            title="Зоны обслуживания"
            features={[
              { label: 'Высота стоек в норме', value: service.counter_height_ok },
            ]}
          />
        )}
      </div>

      {/* Reviews */}
      <section>
        <h2 className="text-xl font-bold text-slate-900 mb-4">
          Отзывы ({reviews.length})
        </h2>

        {user ? (
          <form
            onSubmit={submitReview}
            className="bg-white border rounded-xl p-5 mb-5 space-y-3"
          >
            <div className="flex items-center gap-3">
              <span className="text-sm text-slate-700">Оценка:</span>
              <Stars value={rating} onChange={setRating} />
            </div>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="..."
              rows={3}
              required
              className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none"
            />
            <div className="flex items-center gap-3">
              <label className="inline-flex items-center gap-2 text-sm text-slate-600 cursor-pointer">
                <span className="px-3 py-1.5 border rounded-md hover:bg-slate-50">
                  {photo ? '📎 Заменить фото' : '📎 Добавить фото'}
                </span>
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => setPhoto(e.target.files?.[0] || null)}
                  className="hidden"
                />
              </label>
              {photo && (
                <>
                  <span className="text-xs text-slate-500 truncate max-w-[200px]">
                    {photo.name}
                  </span>
                  <button
                    type="button"
                    onClick={() => setPhoto(null)}
                    className="text-xs text-red-500 hover:underline"
                  >
                    удалить
                  </button>
                </>
              )}
            </div>
            {submitErr && (
              <div className="text-sm text-red-600">{submitErr}</div>
            )}
            <button
              type="submit"
              disabled={submitting || !text.trim()}
              className="px-4 py-2 bg-brand-600 hover:bg-brand-700 disabled:opacity-60 text-white rounded transition"
            >
              {submitting ? t('common.sending') : t('common.send')}
            </button>
          </form>
        ) : (
          <div className="bg-slate-50 border rounded-xl p-4 mb-5 text-sm text-slate-600">
            <Link to="/login" className="text-brand-600 hover:underline">
              {t('nav.login')}
            </Link>
          </div>
        )}

        <div className="space-y-3">
          {reviews.map((r) => (
            <div key={r.id} className="bg-white border rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-3">
                  <Stars value={r.rating} />
                  {r.author_name && (
                    <span className="text-sm text-slate-600">
                       {r.author_name}
                    </span>
                  )}
                </div>
                <span className="text-xs text-slate-500">
                   {new Date(r.created_at).toLocaleDateString('ru-RU')}
                </span>
              </div>
              <p className="text-sm text-slate-800 whitespace-pre-line">{r.text}</p>
              {r.photo && (
                <img
                  src={r.photo}
                  alt=""
                  className="mt-3 max-h-48 rounded border"
                  loading="lazy"
                />
              )}
            </div>
          ))}
          {reviews.length === 0 && (
            <p className="text-sm text-slate-500 text-center py-6">
              Отзывов пока нет
            </p>
          )}
        </div>
      </section>
    </div>
  )
}
