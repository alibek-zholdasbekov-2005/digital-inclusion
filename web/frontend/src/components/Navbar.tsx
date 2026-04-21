import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../store/auth'

const navClass = ({ isActive }: { isActive: boolean }) =>
  `px-3 py-2 rounded-md text-sm font-medium transition ${
    isActive
      ? 'bg-brand-50 text-brand-700'
      : 'text-slate-600 hover:text-brand-600 hover:bg-slate-100'
  }`

export default function Navbar() {
  const { user, signOut } = useAuth()
  const navigate = useNavigate()

  const onLogout = () => {
    signOut()
    navigate('/login')
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
            Карта
          </NavLink>
          <NavLink to="/objects" className={navClass}>
            Объекты
          </NavLink>
          <NavLink to="/forum" className={navClass}>
            Форум
          </NavLink>
          {user && (
            <NavLink to="/favorites" className={navClass}>
              ♡ Избранное
            </NavLink>
          )}
        </nav>

        <div className="flex items-center gap-2">
          {user ? (
            <>
              <NavLink to="/profile" className={navClass}>
                {user.username}
              </NavLink>
              <button
                onClick={onLogout}
                className="px-3 py-2 rounded-md text-sm font-medium text-slate-600 hover:text-red-600 hover:bg-red-50 transition"
              >
                Выйти
              </button>
            </>
          ) : (
            <>
              <NavLink to="/login" className={navClass}>
                Войти
              </NavLink>
              <NavLink
                to="/register"
                className="px-3 py-2 rounded-md text-sm font-medium bg-brand-600 text-white hover:bg-brand-700 transition"
              >
                Регистрация
              </NavLink>
            </>
          )}
        </div>
      </div>
    </header>
  )
}
