# Digital Inclusion — Отчёт по финальному проекту

**Курс:** Intelligent Cloud & Data Processing based on Huawei Technologies
**Студент:** Жолдасбеков Алибек
**Проект:** Digital Inclusion — Доступный Алматы

---

## 1. Идея и актуальность

Digital Inclusion — информационная система паспортизации объектов городской инфраструктуры Алматы с точки зрения **доступности для маломобильных граждан (МГН)**. Пользователи видят на карте города общественные здания и остановки, смотрят, какие элементы доступности присутствуют (пандус, шрифт Брайля, тактильная плитка, индукционная петля и т. д.), оставляют отзывы и обсуждают вопросы доступности на форуме.

Проект решает реальную задачу — в Казахстане нет публичной базы данных доступности объектов, а действующий городской реестр не имеет мобильного/веб-интерфейса для обычных граждан.

## 2. Архитектура

```
                                ┌────────────────────────────┐
   Android (Kotlin) ────────┐   │     Render PaaS (Docker)   │
                            │   │                            │
                            ├──►│  backend-inclusion.onren…  │
                            │   │  Django 5 + DRF + JWT      │
   Web (React SPA)  ────────┘   │          │                 │
                                │          ▼                 │
                                │  Supabase PostGIS DB       │
                                │  Cloudinary (media)        │
                                └────────────────────────────┘
```

**Ключевые принципы:**
1. **Один backend — два клиента.** Мобильное и веб-приложение обращаются к одному и тому же REST API (`https://backend-inclusion.onrender.com`). Это исключает дублирование бизнес-логики.
2. **Разделение репозитория.** В корне три независимые папки: `backend/`, `front_app/` (Kotlin/Android), `front_web/` (React). Разработка мобильной и веб-версии ведётся параллельно и не мешает друг другу.
3. **Контейнеризация всего.** Backend и веб — многостадийные Docker-образы; БД — контейнер `postgis/postgis:15-3.3`. Корневой `docker-compose.yml` поднимает всю систему одной командой.
4. **Statelessness frontend.** SPA не хранит серверного состояния: при каждом запуске подтягивает данные по API, аутентификация — через JWT (access + refresh) в `localStorage`, обновление токена — прозрачно через axios-интерсептор.

## 3. Стек и обоснование

| Компонент    | Выбор                                          | Обоснование                                                    |
|--------------|------------------------------------------------|----------------------------------------------------------------|
| Web-framework| **React 18 + Vite + TypeScript**               | Индустриальный стандарт, быстрый HMR, типобезопасность         |
| Стили        | **TailwindCSS**                                | Утилитарный подход, минимум CSS-файлов, высокий темп           |
| Карта        | **Leaflet + react-leaflet** + OpenStreetMap    | Бесплатно, без API-ключа, работает с GeoJSON из PostGIS        |
| Состояние    | **Zustand**                                    | Минимум бойлерплейта vs Redux                                  |
| HTTP         | **Axios** + interceptors                       | Автоматический refresh JWT на 401                              |
| Backend      | **Django 5 + DRF + simplejwt + drf-spectacular**| Уже есть, OpenAPI схема генерируется автоматически             |
| БД           | **PostgreSQL + PostGIS**                       | Геопространственные запросы (`/api/objects/nearby/`)           |
| Web-сервер   | **nginx (alpine)**                             | Раздача статики SPA + корректный fallback на `index.html`      |
| Хостинг      | **Render**                                     | Нативная поддержка Dockerfile, HTTPS и публичный URL бесплатно |
| CI           | **GitHub Actions**                             | Бесплатно для публичных репо, встроенная интеграция с GitHub   |

## 4. Функционал веб-версии

- **Аутентификация.** JWT через `/api/token/` и `/api/register/`. Refresh-токен автоматически обновляется при 401 через axios-интерсептор.
- **Карта Алматы** (`/`). Точки объектов и остановок, отрисованные поверх OpenStreetMap. Кликабельные попапы с переходом на детали объекта.
- **Список объектов** (`/objects`). Поиск по названию через endpoint `/api/search/?q=`, плитка с кратким описанием.
- **Карточка объекта** (`/objects/:id`). Показывает **все 6 разделов доступности** (вход, пути движения, территория, инфокоммуникации, санитарные комнаты, зоны обслуживания) с иконками ✓/−, фотогалерею и блок отзывов.
- **Отзывы.** Авторизованный пользователь ставит оценку 1–5 звёзд и пишет комментарий; отзывы приходят от всех пользователей системы.
- **Форум** (`/forum`). Темы + сообщения. Авторизованный может создать тему и ответить в любую.
- **Профиль** (`/profile`). Редактирование email текущего пользователя.

## 5. Docker и compose

**Frontend Dockerfile** — multi-stage:

```dockerfile
# Stage 1: node:20-alpine → npm install → vite build
# Stage 2: nginx:1.27-alpine → раздача /usr/share/nginx/html
```

Результат: итоговый образ ~40 MB (без Node в рантайме), VITE_API_BASE_URL
«запекается» в бандл на этапе сборки через `ARG`.

**Корневой `docker-compose.yml`** поднимает три сервиса:

- `db` — `postgis/postgis:15-3.3` с healthcheck через `pg_isready`
- `backend` — Django + gunicorn на 8000, зависит от healthy `db`, автоматически прогоняет migrate + collectstatic
- `web` — nginx с React SPA на 8080

Команда `docker compose up --build` поднимает всё одной строкой.

## 6. Деплой

1. **Backend** — уже на Render (`https://backend-inclusion.onrender.com`). Использует Supabase как PostGIS-БД и Cloudinary для медиа. CORS открыт, `ALLOWED_HOSTS` содержит `.onrender.com`. Все 17 endpoints протестированы через Swagger.
2. **Frontend** — деплоится на Render из `render.yaml` (Blueprint). Render забирает Dockerfile из `./front_web/`, билдит образ, выдаёт публичный HTTPS URL. Healthcheck — `GET /healthz` (отвечает nginx).
3. **Автодеплой.** `autoDeploy: true` в `render.yaml` — каждый push в `main` триггерит пересборку на Render.

## 7. CI/CD

`.github/workflows/ci.yml` при каждом push/PR:

1. **Frontend job:** устанавливает Node 20, ставит зависимости, выполняет `npm run build` (tsc + vite), собирает Docker-образ через Buildx (без push).
2. **Backend job:** собирает backend Docker-образ через Buildx.

CI падает — мердж в main блокируется (если настроить branch protection). Сам Render подхватывает успешный push автоматически.

## 8. Выполнение требований

| Требование                                | Статус |
|-------------------------------------------|--------|
| Приложение в Docker-контейнере            | ✅ Frontend и backend в Docker     |
| Публичный URL                             | ✅ Backend + Frontend на Render    |
| Git-репозиторий                           | ✅ github.com/alibek-zholdasbekov-2005/digital-inclusion |
| Отчёт 2–4 страницы                        | ✅ этот файл                        |
| **Бонус:** CI/CD                          | ✅ GitHub Actions                   |
| **Бонус:** Микросервисы                   | ✅ Backend + Web + DB — независимые сервисы |
| **Бонус:** Контейнер БД                   | ✅ PostGIS в compose                |
| **Бонус:** HTTPS                          | ✅ Render автоматически             |
| **Бонус:** Мобильное приложение           | ✅ Kotlin Android в `front_app/`    |

## 9. Ограничения и следующие шаги

- **Render Free plan** засыпает после 15 минут простоя. Первый запрос после сна занимает ~30 секунд. Для продакшена — Starter plan ($7/мес) без засыпания.
- **Leaflet без кластеризации.** При >500 точек на карте появятся тормоза — следующий шаг: `react-leaflet-cluster`.
- **Нет e2e-тестов.** В CI собирается только сборка. Следующий шаг: Playwright-smoke на ключевых сценариях.
- **Нет push-уведомлений** для новых сообщений форума. Обсуждается Firebase Cloud Messaging для мобилки.

## 10. Ссылки

- Исходный код: <https://github.com/alibek-zholdasbekov-2005/digital-inclusion>
- Backend API: <https://backend-inclusion.onrender.com>
- Swagger: <https://backend-inclusion.onrender.com/api/docs/>
- Веб-версия: будет выдан публичный URL после первого деплоя из `render.yaml`
