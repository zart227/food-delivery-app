# Сервис доставки еды

Проект представляет собой полнофункциональный сервис доставки еды с микросервисной архитектурой.

## Технологический стек

### Backend
- Python 3.12
- Django 5.1
- Django REST Framework
- Celery
- Redis
- PostgreSQL
- Nginx
- Gunicorn (для production)

### Frontend
- Vue.js 3
- Vite
- Pinia
- Vue Router
- SCSS

### Мониторинг и логирование
- Prometheus
- Grafana
- Node Exporter
- Nginx Exporter
- Flower (для мониторинга Celery)

## Основные функции

- Регистрация и авторизация пользователей с подтверждением email
- Каталог блюд с фильтрацией и поиском
- Корзина покупок
- Оформление заказов
- Отслеживание статуса заказа
- Система уведомлений (email)
- Административная панель
- Мониторинг системы

## Установка и запуск

### Требования
- Docker
- Docker Compose

### Разработка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

3. Запустите проект в режиме разработки:
```bash
docker compose -f docker-compose.dev.yml up -d
```

Сервисы будут доступны по следующим адресам:
- Frontend: http://localhost:8081
- API: http://localhost:8081/api/
- Admin панель: http://localhost:8081/admin/
- Swagger: http://localhost:8081/swagger/
- Flower (мониторинг Celery): http://localhost:5555
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090

### Production

1. Настройте переменные окружения в `.env`:
```bash
cp .env.example .env
```

2. Запустите проект:
```bash
docker compose up -d
```

## Автоматическая инициализация

При первом запуске автоматически выполняются следующие операции:
- Применение миграций базы данных
- Создание суперпользователя (если не существует)
- Заполнение базы данных начальными продуктами (если база пуста)

### Учетные данные по умолчанию

#### Development
- Admin панель:
  - Логин: admin
  - Email: admin@example.com
  - Пароль: admin

#### Production
Учетные данные настраиваются через переменные окружения:
- DJANGO_SUPERUSER_USERNAME
- DJANGO_SUPERUSER_EMAIL
- DJANGO_SUPERUSER_PASSWORD

## Мониторинг

### Grafana
- Доступ: http://localhost:3000
- Логин: admin
- Пароль: admin

Предварительно настроенные дашборды:
- Nginx статистика
- Системные метрики
- Метрики Django
- Мониторинг Celery

### Prometheus
- Доступ: http://localhost:9090
- Собирает метрики со следующих экспортеров:
  - Node Exporter (системные метрики)
  - Nginx Exporter
  - Django metrics
  - Celery metrics (через Flower)

### Flower
- Доступ: http://localhost:5555
- Мониторинг задач Celery
- Статистика воркеров
- Мониторинг очередей

## Логирование

- Nginx логи: `nginx/logs/`
- Django логи: через stdout контейнера
- Celery логи: через stdout контейнера и Flower

## Тестирование

```bash
# Запуск тестов
docker compose -f docker-compose.dev.yml exec django python manage.py test
```
