import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL, 
  headers: {
    'Content-Type': 'application/json',
  },
});

// Лог для проверки baseURL
console.log('VITE_API_BASE_URL:', import.meta.env.VITE_API_BASE_URL);

// Добавление токена в заголовки
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
