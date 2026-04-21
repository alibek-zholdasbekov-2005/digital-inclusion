import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../store/auth'
import { useTranslation } from 'react-i18next'

const navClass = ({ isActive }: { isActive: boolean }) =>
  `px-3 py-2 rounded-md text-sm font-medium transition ${
    isActive
      ? 'bg-brand-50 text-brand-700'
      : 'text-slate-600 hover:text-brand-600 hover:bg-slate-100'
  }`

export default function Navbar() {
  const { user, signOut } = useAuth()
  const navigate = useNavigate()
  const { t, i18n } = useTranslation()

  const onLogout = () => {
    signOut()
    navigate('/login')
  }

  const changeLang = (e: React.ChangeEvent<HTMLSelectElement>) => {
    i18n.changeLanguage(e.target.value)
  }

  return (
    <header className="border-b bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center gap-4">
        <Link
          to="/"
          className="flex items-center gap-2 font-bold text-brand-700 text-lg"
        >
          <span className="inline-flex w-8 h-8 rounded-full bg-brand-600 text-white items-center justify-center">
            DI
          </span>
          <span className="hidden sm:inline">Digital Inclusion</span>
        </Link>

        <nav className="flex-1 flex items-center gap-1">
          <NavLink to="/" end className={navClass}>
            {t('nav.map')}
          </NavLink>
          <NavLink to="/objects" className={navClass}>
            {t('nav.objects')}
          </NavLink>
          <NavLink to="/forum" className={navClass}>
            {t('nav.forum')}
          </NavLink>
          {user && (
            <NavLink to="/favorites" className={navClass}>
              {t('nav.favorites')}
            </NavLink>
          )}
        </nav>

        <div className="flex items-center gap-2">
          <select 
            className="text-sm bg-slate-50 border-slate-200 text-slate-700 rounded mr-2 focus:ring-brand-500 focus:border-brand-500" 
            value={i18n.language} 
            onChange={changeLang}
          >
            <option value="ru">Рус</option>
            <option value="en">Eng</option>
            <option value="kk">Қаз</option>
          </select>

          {user ? (
            <>
              <NavLink to="/profile" className={navClass}>
                {user.username}
              </NavLink>
              <button
                onClick={onLogout}
                className="px-3 py-2 rounded-md text-sm font-medium text-slate-600 hover:text-red-600 hover:bg-red-50 transition"
              >
                {t('nav.logout')}
              </button>
            </>
          ) : (
            <>
              <NavLink to="/login" className={navClass}>
                {t('nav.login')}
              </NavLink>
              <NavLink
                to="/register"
                className="px-3 py-2 rounded-md text-sm font-medium bg-brand-600 text-white hover:bg-brand-700 transition"
              >
                {t('nav.register')}
              </NavLink>
            </>
          )}
        </div>
      </div>
    </header>
  )
}
