import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { listObjects, searchObjects } from '../api/objects'
import { listDistricts, listCategories } from '../api/directories'
import type {
  AccessibilityObjectSummary,
  District,
  Category,
} from '../types'
import Spinner from '../components/Spinner'

export default function ObjectList() {
  const { t, i18n } = useTranslation()
  const [objects, setObjects] = useState<AccessibilityObjectSummary[]>([])
  const [districts, setDistricts] = useState<District[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [query, setQuery] = useState('')
  const [districtId, setDistrictId] = useState<number | ''>('')
  const [categoryId, setCategoryId] = useState<number | ''>('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Load dictionaries once
  useEffect(() => {
    listDistricts().then(setDistricts).catch(() => setDistricts([]))
    listCategories().then(setCategories).catch(() => setCategories([]))
  }, [])

  // Initial list
  useEffect(() => {
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  async function load() {
    setLoading(true)
    setError(null)
    try {
      let data: AccessibilityObjectSummary[]
      if (query.trim()) {
        data = await searchObjects(query.trim())
        // search endpoint doesn't support filters, filter client-side
        if (districtId) data = data.filter((o) => o.district === districtId)
        if (categoryId) data = data.filter((o) => o.category === categoryId)
      } else {
        data = await listObjects({
          district: districtId || undefined,
          category: categoryId || undefined,
        })
      }
      setObjects(data)
    } catch {
      setError(t('common.error'))
    } finally {
      setLoading(false)
    }
  }

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    load()
  }

  const resetFilters = () => {
    setQuery('')
    setDistrictId('')
    setCategoryId('')
    setTimeout(load, 0)
  }

  const activeFilters = (districtId ? 1 : 0) + (categoryId ? 1 : 0) + (query ? 1 : 0)

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-slate-900">{t('objects.title')}</h1>
        {activeFilters > 0 && (
          <button
            onClick={resetFilters}
            className="text-sm text-slate-500 hover:text-brand-600"
          >
            {t('objects.reset_filters')} ({activeFilters})
          </button>
        )}
      </div>

      <form
        onSubmit={onSubmit}
        className="bg-white border rounded-lg p-4 mb-6 grid gap-3 md:grid-cols-4"
      >
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={t('home.search_placeholder')}
          className="md:col-span-2 px-3 py-2 border rounded-md focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none"
        />
        <select
          value={districtId}
          onChange={(e) => setDistrictId(e.target.value ? Number(e.target.value) : '')}
          className="px-3 py-2 border rounded-md focus:ring-2 focus:ring-brand-500 outline-none bg-white"
        >
          <option value="">{t('home.district_all')}</option>
          {districts.map((d) => (
            <option key={d.id} value={d.id}>
              {i18n.language === 'en' ? d.name_en || d.name_ru : i18n.language === 'kk' ? d.name_kk || d.name_ru : d.name_ru}
            </option>
          ))}
        </select>
        <select
          value={categoryId}
          onChange={(e) => setCategoryId(e.target.value ? Number(e.target.value) : '')}
          className="px-3 py-2 border rounded-md focus:ring-2 focus:ring-brand-500 outline-none bg-white"
        >
          <option value="">{t('home.category_all')}</option>
          {categories.map((c) => (
            <option key={c.id} value={c.id}>
              {i18n.language === 'en' ? c.name_en || c.name_ru : i18n.language === 'kk' ? c.name_kk || c.name_ru : c.name_ru}
            </option>
          ))}
        </select>
        <button
          type="submit"
          className="md:col-span-4 px-5 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-md transition"
        >
          {t('objects.apply')}
        </button>
      </form>

      {loading && <Spinner />}

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 text-sm px-3 py-2 rounded mb-4">
          {error}
        </div>
      )}

      {!loading && !error && (
        <>
          <p className="text-sm text-slate-600 mb-3">
            {t('objects.found', { length: objects.length })}
          </p>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {objects.map((obj) => (
              <Link
                key={obj.id}
                to={`/objects/${obj.id}`}
                className="block bg-white border rounded-lg p-4 hover:shadow-md hover:border-brand-300 transition"
              >
                <div className="flex items-start justify-between gap-2 mb-1">
                  <h3 className="font-semibold text-slate-900 line-clamp-2 flex-1">
                    {i18n.language === 'en' ? obj.name_en || obj.name_ru : i18n.language === 'kk' ? obj.name_kk || obj.name_ru : obj.name_ru || 'Без названия'}
                  </h3>
                  {typeof obj.avg_rating === 'number' && (
                    <span className="shrink-0 inline-flex items-center gap-1 text-xs bg-yellow-50 text-yellow-700 px-2 py-0.5 rounded-full">
                      ★ {obj.avg_rating.toFixed(1)}
                    </span>
                  )}
                </div>
                <div className="flex flex-wrap gap-1 mb-2">
                  {obj.category_info && (
                    <span
                      className="text-xs px-2 py-0.5 rounded-full"
                      style={{
                        backgroundColor: `${obj.category_info.color || '#2196F3'}20`,
                        color: obj.category_info.color || '#2196F3',
                      }}
                    >
                      {i18n.language === 'en' ? obj.category_info.name_en || obj.category_info.name_ru : i18n.language === 'kk' ? obj.category_info.name_kk || obj.category_info.name_ru : obj.category_info.name_ru}
                    </span>
                  )}
                  {obj.district_name && (
                    <span className="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
                      {obj.district_name}
                    </span>
                  )}
                </div>
                {obj.accessibility_summary && (
                  <p className="text-xs text-slate-500 line-clamp-2">
                    {obj.accessibility_summary}
                  </p>
                )}
                <div className="mt-2 text-xs text-brand-600">Подробнее →</div>
              </Link>
            ))}
          </div>

          {objects.length === 0 && (
            <div className="text-center py-12 text-slate-500">
              {t('objects.not_found')}
            </div>
          )}
        </>
      )}
    </div>
  )
}
