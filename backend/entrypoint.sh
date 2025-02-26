#!/bin/sh

# Запуск миграций и создание суперпользователя только для Django
if [ "$SERVICE_NAME" = "django" ]; then
    echo "⏳ Ожидание доступности базы данных..."
    while ! nc -z "$DB_HOST" "$DB_PORT"; do
        sleep 1
    done
    echo "✅ База данных доступна!"

    echo "🔄 Применение миграций..."
    python manage.py migrate
    python manage.py populate_products

    echo "🔍 Проверка существования суперпользователя..."
    SUPERUSER_EXISTS=$(python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
exists = User.objects.filter(username="$DJANGO_SUPERUSER_USERNAME").exists()
print("EXISTS" if exists else "MISSING")
EOF
    )

    echo "Экземпляр суперпользователя: $SUPERUSER_EXISTS"

    if [ "$SUPERUSER_EXISTS" = "MISSING" ]; then
        echo "🆕 Создание суперпользователя $DJANGO_SUPERUSER_USERNAME..."
        python manage.py createsuperuser --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL" --noinput
    fi
fi

# Запуск соответствующих сервисов
case "$SERVICE_NAME" in
    "django")
        echo "🚀 Запуск Gunicorn..."
        # Добавление автоматической перезагрузки при изменениях
        if [ "$ENVIRONMENT" = "development" ]; then
            echo "🚀 Запуск в режиме разработки..."
            watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 3 --chdir /app &
        else
            echo "🚀 Запуск в production режиме..."
            gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 3 --chdir /app &
        fi
        echo "🚀 Запуск Nginx..."
        nginx -g 'daemon off;'
        ;;
    "celery")
        echo "🚀 Запуск Celery Worker..."
        celery -A backend worker --loglevel=info
        ;;
    "celery-beat")
        echo "🚀 Запуск Celery Beat..."
        celery -A backend beat --loglevel=info
        ;;
    *)
        echo "Неизвестный сервис: $SERVICE_NAME"
        exit 1
        ;;
esac