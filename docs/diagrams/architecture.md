# Архитектура Food Delivery Service

```mermaid
graph TB
    %% Определение стилей
    classDef frontend fill:#42b883,stroke:#35495e,color:white
    classDef backend fill:#3775a9,stroke:#2a5f8a,color:white
    classDef database fill:#336791,stroke:#2a5577,color:white
    classDef cache fill:#dc382d,stroke:#9a1b1b,color:white
    classDef queue fill:#ff6b6b,stroke:#cc5757,color:white
    classDef proxy fill:#009639,stroke:#007a2e,color:white
    classDef monitoring fill:#f5a623,stroke:#d48c1f,color:white

    %% Клиентская часть
    Client[Браузер/Клиент]
    
    %% Прокси и балансировка
    Nginx[Nginx Proxy/Load Balancer]:::proxy
    
    %% Frontend приложение
    Vue[Vue.js Frontend<br/>Vite + Pinia]:::frontend
    
    %% Backend сервисы
    Django[Django Backend<br/>DRF + Channels]:::backend
    Celery[Celery Workers]:::queue
    
    %% База данных и кеширование
    Postgres[(PostgreSQL)]:::database
    Redis[(Redis<br/>Cache + Queue)]:::cache
    
    %% Мониторинг
    Prometheus[Prometheus<br/>Metrics]:::monitoring
    Grafana[Grafana<br/>Dashboards]:::monitoring

    %% Определение связей
    Client --> Nginx
    Nginx --> Vue
    Nginx --> Django
    Django --> Postgres
    Django --> Redis
    Django --> Celery
    Celery --> Redis
    Celery --> Postgres
    
    %% Мониторинг связи
    Django -.-> Prometheus
    Celery -.-> Prometheus
    Nginx -.-> Prometheus
    Prometheus -.-> Grafana

    %% Подписи к связям
    Client -- "HTTPS" --> Nginx
    Nginx -- "Статика" --> Vue
    Nginx -- "API запросы" --> Django
    Django -- "WebSocket" --> Client
    Django -- "Запись/Чтение" --> Postgres
    Django -- "Кеширование" --> Redis
    Django -- "Асинхронные задачи" --> Celery
    Celery -- "Очереди" --> Redis
```

## Описание компонентов

### Frontend (Vue.js)
- Single Page Application на Vue 3
- State Management с Pinia
- Сборка через Vite
- Компоненты UI с TailwindCSS

### Backend (Django)
- REST API через Django REST Framework
- WebSocket для real-time обновлений
- JWT аутентификация
- Асинхронные задачи

### Очереди и кеширование
- Celery для обработки асинхронных задач
- Redis как брокер сообщений
- Кеширование данных в Redis

### База данных
- PostgreSQL для хранения данных
- Миграции Django ORM
- Индексация для оптимизации запросов

### Прокси и балансировка
- Nginx как reverse proxy
- Балансировка нагрузки
- SSL/TLS терминация
- Раздача статики

### Мониторинг
- Prometheus для сбора метрик
- Grafana для визуализации
- Алертинг и оповещения

## Основные потоки данных

1. **Запросы клиентов**
   - HTTPS запросы через Nginx
   - WebSocket соединения для real-time обновлений
   - Статические файлы через Nginx

2. **Обработка заказов**
   - Создание через REST API
   - Асинхронная обработка в Celery
   - Уведомления через WebSocket

3. **Кеширование**
   - Кеширование частых запросов
   - Сессии в Redis
   - Очереди задач

4. **Мониторинг**
   - Сбор метрик со всех сервисов
   - Визуализация в Grafana
   - Система алертинга 