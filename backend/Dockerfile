# Base Stage: Установка зависимостей
FROM python:3.12 as base
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential nginx
RUN pip3 install --upgrade pip
COPY pyproject.toml poetry.lock ./
RUN pip3 install poetry && poetry config virtualenvs.create false && poetry install --no-dev

# Stage 1: Build static files
FROM base as django-build
COPY . /app

RUN python manage.py collectstatic --noinput

# Stage 2: Nginx + Gunicorn
FROM base as django-server
COPY --from=django-build /app /app
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Создание сокета Gunicorn
RUN mkdir -p /run/gunicorn && chown -R www-data:www-data /run/gunicorn

EXPOSE 80
CMD ["sh", "-c", "\
    python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py populate_products && \
    gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 3 --chdir /app & \
    nginx -g 'daemon off;'"]

