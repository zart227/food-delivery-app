import api from './axios';
import { refreshToken, logout } from '../services/authService';

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true; // Помечаем запрос, чтобы избежать бесконечной петли
      try {
        const newAccessToken = await refreshToken();
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest); // Повторяем запрос
      } catch (refreshError) {
        console.error('Не удалось обновить токен:', refreshError);
        logout(); // Выход пользователя при истечении refresh токена
      }
    }
    return Promise.reject(error);
  }
);
