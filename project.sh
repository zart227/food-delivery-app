#!/bin/bash

set -e

show_menu() {
  echo "\n===== Меню управления проектом ====="
  echo "1) Запустить проект (dev)"
  echo "2) Остановить проект (dev)"
  echo "3) Запустить проект (prod)"
  echo "4) Остановить проект (prod)"
  echo "5) Перезапустить backend"
  echo "6) Перезапустить frontend"
  echo "7) Логи backend"
  echo "8) Логи frontend"
  echo "9) Запустить тесты backend"
  echo "10) Запустить тесты frontend"
  echo "11) Создать суперпользователя"
  echo "12) Очистить Docker окружение (опасно)"
  echo "13) Очистить логи Docker (Linux)"
  echo "0) Выйти"
  echo "===================================="
}

run_dev() {
  docker compose -f docker-compose.dev.yml up -d
}

stop_dev() {
  docker compose -f docker-compose.dev.yml down
}

run_prod() {
  docker compose -f docker-compose.prod.yml up -d
}

stop_prod() {
  docker compose -f docker-compose.prod.yml down
}

restart_backend() {
  docker compose stop django && docker compose rm -f django && docker compose build django && docker compose up -d django && docker compose logs -f django
}

restart_frontend() {
  docker compose stop frontend && docker compose rm -f frontend && docker compose build frontend && docker compose up -d frontend && docker compose logs -f frontend
}

logs_backend() {
  docker compose logs -f django
}

logs_frontend() {
  docker compose logs -f frontend
}

test_backend() {
  docker compose -f docker-compose.dev.yml exec django python manage.py test
}

test_frontend() {
  docker compose -f docker-compose.dev.yml exec frontend yarn test || echo "Нет тестов или не настроены."
}

create_superuser() {
  bash create_superuser.sh
}

clean_docker() {
  bash clean_docker.sh
}

clear_docker_logs() {
  echo "Очистка логов Docker (требуются права sudo)..."
  sudo sh -c 'truncate -s 0 /var/lib/docker/containers/*/*-json.log'
  echo "Логи Docker очищены."
}

while true; do
  show_menu
  read -p "Выберите действие: " choice
  case $choice in
    1) run_dev ;;
    2) stop_dev ;;
    3) run_prod ;;
    4) stop_prod ;;
    5) restart_backend ;;
    6) restart_frontend ;;
    7) logs_backend ;;
    8) logs_frontend ;;
    9) test_backend ;;
    10) test_frontend ;;
    11) create_superuser ;;
    12) clean_docker ;;
    13) clear_docker_logs ;;
    0) echo "Выход."; exit 0 ;;
    *) echo "Неверный выбор!" ;;
  esac
done 