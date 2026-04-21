# Digital Inclusion — Web

Веб-версия проекта. Независимая от мобильной ветки (`backend/` + `front_app/`
в корне репозитория). Деплоится отдельными сервисами на Render через корневой
`render.yaml`.

## Структура

```
web/
├── backend/           # Django + DRF + PostGIS (копия)
├── frontend/          # React + Vite + TS + Tailwind + Leaflet
└── docker-compose.yml # локальный стек (db + backend + frontend)
```

## Локальный запуск

```bash
docker compose -f web/docker-compose.yml up --build
# frontend → http://localhost:8080
# backend  → http://localhost:8000/api/docs/
```

## Деплой на Render

Корневой `render.yaml` создаёт три ресурса:
- `web-db` — управляемая БД PostGIS
- `web-backend` — Django-сервис
- `web-frontend` — nginx со статикой React

После первого деплоя прописать в переменных:
- `web-backend.CORS_ALLOWED_ORIGINS` = URL фронта
- `web-frontend.VITE_API_BASE_URL` = URL бэка
- Cloudinary ключи (`CLOUDINARY_*`) на бэке

## Модули по ТЗ

1. Главная с картой — `frontend/src/pages/Home.tsx`, Leaflet + фильтры район/категория
2. Паспортизация — `POST /api/objects/` (+ admin)
3. Избранные — `frontend/src/pages/Favorites.tsx`, `/api/favorites/`
4. Профиль — `frontend/src/pages/Profile.tsx`, `/api/me/`
5. Форум — `frontend/src/pages/Forum.tsx`, `/api/forum/topics/` и `/posts/`
6. Отзывы/оценки — на `ObjectDetail`, `/api/reviews/`
