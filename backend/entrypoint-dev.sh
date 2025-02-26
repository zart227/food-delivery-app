#!/bin/bash

# Ждем, пока postgres будет доступен
while ! nc -z postgres 5432; do
    echo "Waiting for postgres..."
    sleep 1
done

# Применяем миграции
python manage.py migrate

# Запускаем Django dev сервер с автоперезагрузкой
if [ "$SERVICE_NAME" = "django" ]; then
    watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- python manage.py runserver 0.0.0.0:8000
elif [ "$SERVICE_NAME" = "celery" ]; then
    watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery -A backend worker -l info
elif [ "$SERVICE_NAME" = "celery-beat" ]; then
    watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery -A backend beat -l info
fi 