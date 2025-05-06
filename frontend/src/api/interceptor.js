import api from './axios';
import { refreshToken } from '../services/authService';
import { useAuthStore } from '../stores/auth';
import router from '../router';
import { getAuthToken } from '../utils/cookies';

api.interceptors.request.use((config) => {
  const token = getAuthToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Не делать refresh, если это попытка логина
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      !(originalRequest.url && originalRequest.url.includes('/auth/jwt/create/'))
    ) {
      originalRequest._retry = true;
      
      try {
        const newAccessToken = await refreshToken();
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        console.error('Не удалось обновить токен:', refreshError);
        const authStore = useAuthStore();
        await authStore.logoutUser();
        await router.push('/auth');
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);
