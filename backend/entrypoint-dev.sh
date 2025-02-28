#!/bin/bash

# Ждем, пока postgres будет доступен
while ! nc -z postgres 5432; do
    echo "Waiting for postgres..."
    sleep 1
done

# Применяем миграции только в Django сервисе
if [ "$SERVICE_NAME" = "django" ]; then
    echo "Running migrations..."
    python manage.py migrate

    # Собираем статические файлы
    echo "Collecting static files..."
    python manage.py collectstatic --noinput

    # Проверяем наличие продуктов в базе
    PRODUCTS_COUNT=$(python manage.py shell -c "from products.models import Product; print(Product.objects.count())")
    if [ "$PRODUCTS_COUNT" -eq 0 ]; then
        echo "Populating database with products..."
        python manage.py populate_products
    else
        echo "Products already exist in database"
    fi

    # Проверяем наличие суперпользователя
    SUPERUSER_EXISTS=$(python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(is_superuser=True).exists())")
    if [ "$SUPERUSER_EXISTS" = "False" ]; then
        echo "Creating superuser..."
        python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin') if not User.objects.filter(username='admin').exists() else None"
        echo "Superuser created successfully"
    else
        echo "Superuser already exists"
    fi

    watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- python manage.py runserver 0.0.0.0:8000
elif [ "$SERVICE_NAME" = "celery" ]; then
    # Ждем, пока Django применит миграции
    echo "Waiting for Django to be ready..."
    sleep 10
    watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery -A backend worker -l info
elif [ "$SERVICE_NAME" = "celery-beat" ]; then
    # Ждем, пока Django применит миграции
    echo "Waiting for Django to be ready..."
    sleep 10
    watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery -A backend beat -l info
fi 