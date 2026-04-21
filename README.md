# Digital Inclusion — Доступный Алматы (Final Version)

Система паспортизации объектов доступности для маломобильных граждан города Алматы. 

## 🔗 Живые ссылки (Live URLs)
- **Frontend App:** [https://web-frontend-dhwe.onrender.com/](https://web-frontend-dhwe.onrender.com/)
- **Backend API:** [https://web-backend-hgm5.onrender.com/api/objects/](https://web-backend-hgm5.onrender.com/api/objects/)
- **API Documentation (Swagger):** [https://web-backend-hgm5.onrender.com/api/docs/](https://web-backend-hgm5.onrender.com/api/docs/)
- **Health Monitoring:** [https://web-backend-hgm5.onrender.com/api/health/](https://web-backend-hgm5.onrender.com/api/health/)

## 📂 Структура проекта
- `web/backend/` — Django REST API (PostGIS, Python 3.11, JWT).
- `web/frontend/` — React SPA (TypeScript, TailwindCSS, Vite).
- `web/k8s/` — Kubernetes Manifests (Deployments, Services, Ingress).
- `web/docker-compose.yml` — Unified orchestration.
- `.github/workflows/` — CI/CD Pipeline (GitHub Actions).

## 🚀 Основные возможности (Enterprise-ready)
1. **Геопространственные данные**: Использование PostGIS для поиска ближайших доступных объектов.
2. **Мультиязычность**: Полная локализация интерфейса (KK, RU, EN).
3. **Облачная архитектура**: CI/CD автоматизация и готовность к Kubernetes.
4. **Мониторинг**: Встроенный эндпоинт проверки здоровья системы.

## 🛠 Быстрый старт (Docker)
```bash
cd web
docker compose up --build
```
- Web: http://localhost:3000
- Backend: http://localhost:8000

## 📑 Документация
Подробный технический отчет со всеми деталями архитектуры и выполнения требований: [docs/REPORT.md](docs/REPORT.md)
