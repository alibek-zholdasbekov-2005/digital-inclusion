import { useEffect } from 'react'
import { Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import ObjectList from './pages/ObjectList'
import ObjectDetail from './pages/ObjectDetail'
import Forum from './pages/Forum'
import TopicDetail from './pages/TopicDetail'
import Profile from './pages/Profile'
import Favorites from './pages/Favorites'
import NotFound from './pages/NotFound'
import { useAuth } from './store/auth'

export default function App() {
  const init = useAuth((s) => s.init)

  useEffect(() => {
    init()
  }, [init])

  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/objects" element={<ObjectList />} />
        <Route path="/objects/:id" element={<ObjectDetail />} />
        <Route path="/forum" element={<Forum />} />
        <Route path="/forum/:id" element={<TopicDetail />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />
        <Route
          path="/favorites"
          element={
            <ProtectedRoute>
              <Favorites />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  )
}
