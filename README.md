# Digital Inclusion — Доступный Алматы

Система паспортизации объектов доступности для маломобильных граждан города Алматы. Содержит карту объектов и остановок, форум для обсуждений и отзывы.

**Public URLs:**
- Веб-версия: `https://digital-inclusion-web.onrender.com` *(создаётся из `render.yaml`)*
- Backend API: <https://backend-inclusion.onrender.com>
- Swagger: <https://backend-inclusion.onrender.com/api/docs/>
- Админ-панель: <https://backend-inclusion.onrender.com/admin/>

## Репозиторий

```
digital-inclusion/
├── backend/             # Django REST API (Python 3.11, DRF, PostGIS, JWT)
├── front_app/           # Android mobile app (Kotlin)
├── front_web/           # React web app (Vite + TS + Tailwind + Leaflet)
├── docker-compose.yml   # Full stack: db + backend + web
├── render.yaml          # Render Blueprint for the web service
└── .github/workflows/   # GitHub Actions CI (build images)
```

Веб-фронт и мобильное приложение работают с **одним и тем же backend**. Разработка идёт параллельно, клиенты изолированы в своих папках и не мешают друг другу.

## Быстрый старт (Docker)

```bash
# Поднять всё разом (db + backend + web)
docker compose up --build

# Сайт     → http://localhost:8080
# API docs → http://localhost:8000/api/docs/
```

## Только веб (Docker)

```bash
cd front_web
docker build -t di-web .
docker run --rm -p 8080:8080 di-web
```

## Стек

| Слой        | Технологии                                                       |
|-------------|------------------------------------------------------------------|
| Backend     | Django 5, DRF, simplejwt, PostGIS, drf-spectacular, Cloudinary  |
| Web frontend| React 18, Vite, TypeScript, TailwindCSS, react-leaflet, zustand |
| Mobile      | Kotlin, Android                                                  |
| База данных | PostgreSQL + PostGIS                                             |
| Хостинг     | Render (Docker), Supabase (БД), Cloudinary (медиа)              |
| CI/CD       | GitHub Actions                                                   |

## Документация

- Архитектура и деплой: [`docs/REPORT.md`](docs/REPORT.md)
- API: `/api/docs/` (Swagger) и `/api/schema/` (OpenAPI 3.0)

## Команда

- Alibek Zholdasbekov — разработка, архитектура
