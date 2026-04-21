import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { MapContainer, Marker, Popup, TileLayer, CircleMarker } from 'react-leaflet'
import L from 'leaflet'
import { useTranslation } from 'react-i18next'
import { listObjects, listBusStops } from '../api/objects'
import { listCategories, listDistricts } from '../api/directories'
import { parsePoint } from '../api/geo'
import type {
  AccessibilityObjectSummary,
  BusStop,
  Category,
  District,
} from '../types'
import Spinner from '../components/Spinner'

// Fix default marker icons (Leaflet + bundlers)
const defaultIcon = L.icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl:
    'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
})
L.Marker.prototype.options.icon = defaultIcon

const ALMATY_CENTER: [number, number] = [43.2389, 76.8897]

export default function Home() {
  const { t, i18n } = useTranslation()
  const [objects, setObjects] = useState<AccessibilityObjectSummary[]>([])
  const [stops, setStops] = useState<BusStop[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [districts, setDistricts] = useState<District[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showStops, setShowStops] = useState(true)

  // Filters
  const [categoryId, setCategoryId] = useState<number | ''>('')
  const [districtId, setDistrictId] = useState<number | ''>('')

  useEffect(() => {
    let cancelled = false
    async function load() {
      setLoading(true)
      try {
        const [objs, busStops, cats, dists] = await Promise.all([
          listObjects().catch(() => []),
          listBusStops().catch(() => []),
          listCategories().catch(() => []),
          listDistricts().catch(() => []),
        ])
        if (!cancelled) {
          setObjects(objs)
          setStops(busStops)
          setCategories(cats)
          setDistricts(dists)
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
  }, [t])

  const filteredObjects = useMemo(
    () =>
      objects.filter((o) => {
        if (categoryId && o.category !== categoryId) return false
        if (districtId && o.district !== districtId) return false
        return true
      }),
    [objects, categoryId, districtId],
  )

  const objectsWithCoords = useMemo(
    () =>
      filteredObjects
        .map((o) => ({ obj: o, pt: parsePoint(o.location) }))
        .filter(
          (x): x is { obj: AccessibilityObjectSummary; pt: [number, number] } =>
            x.pt !== null,
        ),
    [filteredObjects],
  )

  const stopsWithCoords = useMemo(
    () =>
      stops
        .map((s) => ({ stop: s, pt: parsePoint(s.location) }))
        .filter((x): x is { stop: BusStop; pt: [number, number] } => x.pt !== null),
    [stops],
  )

  return (
    <div className="relative h-[calc(100vh-8rem)]">
      <div className="absolute top-4 left-4 z-[400] bg-white rounded-lg shadow-lg border p-4 max-w-xs">
        <h1 className="text-lg font-bold text-slate-900 mb-1">
          {t('home.title')}
        </h1>
        <p className="text-xs text-slate-600 mb-3">
          Карта объектов и остановок с данными доступности для маломобильных граждан.
        </p>

        <div className="space-y-2 mb-3">
          <select
            value={categoryId}
            onChange={(e) =>
              setCategoryId(e.target.value ? Number(e.target.value) : '')
            }
            className="w-full text-sm px-2 py-1 border rounded"
          >
            <option value="">{t('home.category_all')}</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {i18n.language === 'kk' ? c.name_kz || c.name_ru : c.name_ru}
              </option>
            ))}
          </select>
          <select
            value={districtId}
            onChange={(e) =>
              setDistrictId(e.target.value ? Number(e.target.value) : '')
            }
            className="w-full text-sm px-2 py-1 border rounded"
          >
            <option value="">{t('home.district_all')}</option>
            {districts.map((d) => (
              <option key={d.id} value={d.id}>
                {i18n.language === 'kk' ? d.name_kz || d.name_ru : d.name_ru}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2 text-sm">
          <div className="flex items-center gap-2">
            <span className="inline-block w-3 h-3 rounded-full bg-brand-600 border-2 border-white shadow" />
            <span>{t('nav.objects')} ({objectsWithCoords.length})</span>
          </div>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showStops}
              onChange={(e) => setShowStops(e.target.checked)}
              className="rounded"
            />
            <span className="inline-block w-3 h-3 rounded-full bg-orange-500" />
            <span>Остановки ({stopsWithCoords.length})</span>
          </label>
        </div>
        {error && <div className="mt-3 text-xs text-red-600">{error}</div>}
        <Link
          to="/objects"
          className="mt-3 block text-center text-sm bg-brand-600 hover:bg-brand-700 text-white py-2 rounded transition"
        >
          {t('nav.objects')} →
        </Link>
      </div>

      {loading && (
        <div className="absolute inset-0 bg-white/60 z-[450] flex items-center justify-center">
          <Spinner label={t('common.loading')} />
        </div>
      )}

      <MapContainer
        center={ALMATY_CENTER}
        zoom={12}
        className="h-full w-full"
        scrollWheelZoom
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {objectsWithCoords.map(({ obj, pt }) => {
          const [lon, lat] = pt
          return (
            <Marker key={`obj-${obj.id}`} position={[lat, lon]}>
              <Popup>
                <div className="min-w-[200px]">
                  <div className="font-semibold text-slate-900 mb-1">
                    {/* dynamic names are only stored as name_ru, no name_kz exists on AccessibilityObjectSummary in API currently but we can fallback just in case */}
                    {obj.name_ru || 'Без названия'}
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
                        {/* We don't have name_kz in category_info returned by API either, but let's just use name_ru */}
                        {obj.category_info.name_ru}
                      </span>
                    )}
                    {obj.district_name && (
                      <span className="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
                        {obj.district_name}
                      </span>
                    )}
                  </div>
                  {typeof obj.avg_rating === 'number' && (
                    <div className="text-xs text-yellow-700 mb-1">
                      ★ {obj.avg_rating.toFixed(1)}
                      {obj.reviews_count ? ` (${obj.reviews_count})` : ''}
                    </div>
                  )}
                  {obj.accessibility_summary && (
                    <div className="text-xs text-slate-600 mb-2">
                      {obj.accessibility_summary}
                    </div>
                  )}
                  <Link
                    to={`/objects/${obj.id}`}
                    className="text-brand-600 hover:underline text-sm"
                  >
                    Подробнее →
                  </Link>
                </div>
              </Popup>
            </Marker>
          )
        })}

        {showStops &&
          stopsWithCoords.map(({ stop, pt }) => {
            const [lon, lat] = pt
            return (
              <CircleMarker
                key={`stop-${stop.id}`}
                center={[lat, lon]}
                radius={6}
                pathOptions={{
                  color: '#f97316',
                  fillColor: '#f97316',
                  fillOpacity: 0.8,
                  weight: 2,
                }}
              >
                <Popup>
                  <div>
                    <div className="font-semibold">
                      {stop.stop_name || 'Остановка'}
                    </div>
                    {stop.total_status && (
                      <div className="text-xs text-slate-600">
                        {stop.total_status}
                      </div>
                    )}
                  </div>
                </Popup>
              </CircleMarker>
            )
          })}
      </MapContainer>
    </div>
  )
}
