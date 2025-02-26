# 🛒 Food Delivery Service

## 📌 О проекте
**Food Delivery Service** — это веб-приложение для заказа еды с возможностью онлайн-оплаты и управления заказами. Проект построен на **Django (DRF)** для бэкенда и **Vue 3** для фронтенда, с использованием **Celery + Redis** для обработки фоновых задач.

## 🚀 Функциональность
- **Аутентификация и авторизация** (JWT, OAuth2, Djoser)
- **Каталог продуктов** (по категориям, поиск, фильтры)
- **Корзина** (добавление, удаление, подсчет общей суммы)
- **Оформление заказа** (включая сохранение адреса и оплаты)
- **Система ролей и прав доступа** (пользователи, администраторы)
- **Административная панель** (управление товарами и заказами)
- **Очереди задач** (обработка заказов через Celery + Redis)
- **Кеширование данных** (Redis)
- **WebSockets** (реалтайм-обновления статуса заказов)
- **Докеризация** (backend + frontend + nginx + PostgreSQL + Redis + Celery)

---

## 🏗 Технологии
### Backend:
- **Python 3.12**
- **Django + Django REST Framework (DRF)**
- **PostgreSQL**
- **Celery + Redis** (для обработки фоновых задач)
- **Djoser** (JWT аутентификация)
- **Gunicorn + Nginx**
- **Django Channels** (WebSocket поддержка)

### Frontend:
- **Vue 3 + Pinia**
- **Vite**
- **Vue-Router**
- **Axios**
- **TailwindCSS / Vuetify / Quasar**

### Инфраструктура:
- **Docker + Docker Compose**
- **Nginx** (реверс-прокси)
- **Let's Encrypt** (SSL сертификаты)
- **Celery Beat** (планировщик задач)
- **WebSockets (Django Channels)**

---

## 🔧 Развертывание проекта

### 1️⃣ 📥 Клонирование репозитория:
```bash
git clone https://github.com/zart227/finalProject.git
cd finalProject
```

### 2️⃣ 🛠 Настройка переменных окружения:
Создай файл `.env` в корне проекта и добавь:
```env
# Django
SECRET_KEY="your-secret-key"
DEBUG=True
ALLOWED_HOSTS="*"

# PostgreSQL
POSTGRES_DB=food_delivery
POSTGRES_USER=root
POSTGRES_PASSWORD=yourpassword
DB_HOST=postgres
DB_PORT=5432

# Redis & Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Email (пример для Gmail)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD="your-email-password"

# Frontend URL
FRONTEND_URL=http://localhost:8081

# Domain
DOMAIN=localhost:8081
```

### 3️⃣ 🐳 Запуск проекта

#### Режим разработки (Development):
```bash
docker compose -f docker-compose.dev.yml up --build
```
В этом режиме:
- Автоматическая перезагрузка бэкенда при изменении Python файлов
- Hot-reload для фронтенда (Vite dev server)
- Монтирование исходного кода через volumes
- Отладочные инструменты и логи

#### Режим продакшена (Production):
```bash
docker compose -f docker-compose.prod.yml up --build
```
В этом режиме:
- Оптимизированная сборка фронтенда
- Gunicorn для бэкенда
- Nginx для раздачи статики
- Минимальные логи и отсутствие отладочных инструментов

Проект будет доступен на `http://localhost:8081/`

---

## ⚙️ Управление сервисами

### 📌 Доступ к логам:
```bash
# Все логи
docker compose -f docker-compose.dev.yml logs -f

# Логи конкретного сервиса
docker compose -f docker-compose.dev.yml logs -f django
```

### 📌 Создание суперпользователя:
```bash
docker exec -it django python manage.py createsuperuser
```

### 📌 Работа с миграциями:
```bash
# Создание миграций
docker exec -it django python manage.py makemigrations

# Применение миграций
docker exec -it django python manage.py migrate
```

### 📌 Доступ в контейнеры:
```bash
# Бэкенд
docker exec -it django bash

# Фронтенд
docker exec -it frontend sh
```

---

## 📜 API Документация
После запуска проекта доступна Swagger-документация:
```
http://localhost:8081/api/docs/
```

---

## 🔍 Отладка

### Backend:
- Логи Django доступны в контейнере django
- Debug-toolbar в режиме разработки
- Django Extensions для отладки

### Frontend:
- Vue DevTools в режиме разработки
- Vite Dev Server с hot-reload
- Source maps для отладки

### Мониторинг:
- Celery Flower для мониторинга задач
- Nginx access и error логи
- PostgreSQL логи
