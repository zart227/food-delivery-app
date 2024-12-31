import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api', // Замените на адрес вашего бэка
  headers: {
    'Content-Type': 'application/json',
  },
});

// Добавление токена в заголовки
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
