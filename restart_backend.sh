#!/bin/bash

echo "Остановка контейнера Django..."
docker compose stop django

echo "Удаление контейнера Django..."
docker compose rm -f django

echo "Пересборка образа Django..."
docker compose build django

echo "Запуск контейнера Django..."
docker compose up -d django

echo "Просмотр логов Django..."
docker compose logs -f django