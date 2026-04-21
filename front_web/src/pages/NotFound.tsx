import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="max-w-xl mx-auto px-4 py-20 text-center">
      <h1 className="text-5xl font-bold text-slate-300 mb-2">404</h1>
      <p className="text-lg text-slate-600 mb-6">Страница не найдена</p>
      <Link
        to="/"
        className="inline-block px-5 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded transition"
      >
        На главную
      </Link>
    </div>
  )
}
