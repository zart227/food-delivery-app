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
