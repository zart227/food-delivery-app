# Base Stage: Установка зависимостей
FROM python:3.12 AS base
WORKDIR /app

# Установка зависимостей системы
RUN apt-get update && apt-get install -y build-essential nginx curl netcat-openbsd

# Установка Poetry через официальный скрипт
RUN curl -sSL https://install.python-poetry.org | python3 -

# Добавление Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Копирование файлов проекта
COPY pyproject.toml poetry.lock ./

# Настройка poetry и установка зависимостей
RUN poetry config virtualenvs.create false && poetry install --only main --no-root --no-interaction --no-ansi

# Stage 0: Development stage
FROM base AS dev-stage
WORKDIR /app

# Установка dev-зависимостей
RUN poetry install --only dev --no-root --no-interaction --no-ansi

# Установка watchdog для автоперезагрузки
RUN pip install watchdog[watchmedo]

# Копируем entrypoint-dev.sh и делаем его исполняемым
COPY entrypoint-dev.sh /app/entrypoint-dev.sh
RUN chmod +x /app/entrypoint-dev.sh

CMD ["/app/entrypoint-dev.sh"]

# Stage 1: Build static files
FROM base AS django-build
COPY . /app
RUN python manage.py collectstatic --noinput

# Stage 2: Production stage
FROM base AS django-server
COPY --from=django-build /app /app
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Копируем entrypoint.sh и делаем его исполняемым
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 80
ENTRYPOINT ["/app/entrypoint.sh"]