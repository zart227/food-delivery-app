#!/bin/bash

echo "Загрузка переменных окружения..."
export $(grep -v '^#' .env | xargs)

echo "Запуск команды создания суперпользователя..."

docker compose exec -T django python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()

username = "${DJANGO_SUPERUSER_USERNAME}"
email = "${DJANGO_SUPERUSER_EMAIL}"
password = "${DJANGO_SUPERUSER_PASSWORD}"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✅ Суперпользователь создан успешно!")
else:
    print("ℹ️ Суперпользователь уже существует.")
EOF