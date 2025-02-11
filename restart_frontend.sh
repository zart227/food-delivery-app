#!/bin/bash

echo "Остановка контейнера фронтенда..."
docker compose stop frontend

echo "Удаление контейнера фронтенда..."
docker compose rm -f frontend

echo "Пересборка образа фронтенда..."
docker compose build frontend

echo "Запуск контейнера фронтенда..."
docker compose up -d frontend

echo "Просмотр логов фронтенда..."
docker compose logs -f frontend