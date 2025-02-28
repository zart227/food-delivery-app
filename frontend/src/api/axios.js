import axios from 'axios';
import { getAuthToken } from '../utils/cookies';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Важно для работы с куками
});

// Лог для проверки baseURL
//console.log('VITE_API_BASE_URL:', import.meta.env.VITE_API_BASE_URL);

// Добавление токена в заголовки
api.interceptors.request.use((config) => {
  const token = getAuthToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
