import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

export default function NotFound() {
  const { t } = useTranslation()
  return (
    <div className="max-w-xl mx-auto px-4 py-20 text-center">
      <h1 className="text-5xl font-bold text-slate-300 mb-2">404</h1>
      <p className="text-lg text-slate-600 mb-6">{t('not_found.title')}</p>
      <Link
        to="/"
        className="inline-block px-5 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded transition"
      >
        {t('not_found.go_home')}
      </Link>
    </div>
  )
}
