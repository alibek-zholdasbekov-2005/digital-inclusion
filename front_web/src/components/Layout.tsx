import { Outlet } from 'react-router-dom'
import Navbar from './Navbar'

export default function Layout() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-1">
        <Outlet />
      </main>
      <footer className="border-t bg-white py-4 text-center text-sm text-slate-500">
        © {new Date().getFullYear()} Digital Inclusion — доступный Алматы
      </footer>
    </div>
  )
}
