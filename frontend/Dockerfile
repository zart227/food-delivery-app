# Stage 0: Development stage
FROM node:18-alpine AS dev-stage
WORKDIR /app
COPY package*.json ./
RUN yarn install
# Не копируем исходники в dev-stage, они будут монтироваться через volume
CMD ["yarn", "dev", "--host", "0.0.0.0", "--port", "3000"]

# Stage 1: Build frontend
FROM node:18-alpine AS build-stage
WORKDIR /app
COPY package*.json ./
RUN yarn install
COPY . .
RUN yarn build

# Stage 2: Nginx for serving Vue
FROM nginx:stable-alpine AS vue-server
WORKDIR /usr/share/nginx/html

# Копирование собранного фронта
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Копирование Nginx конфигурации
COPY frontend.nginx.conf /etc/nginx/conf.d/default.conf

# Запуск Nginx
CMD ["nginx", "-g", "daemon off;"]
