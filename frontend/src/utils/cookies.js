export const setCookie = (name, value, expirationMinutes = 30) => {
  const date = new Date();
  date.setTime(date.getTime() + (expirationMinutes * 60 * 1000));
  const expires = `expires=${date.toUTCString()}`;
  document.cookie = `${name}=${value};${expires};path=/;SameSite=Strict`;
};

export const getCookie = (name) => {
  const cookieName = `${name}=`;
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    cookie = cookie.trim();
    if (cookie.indexOf(cookieName) === 0) {
      return cookie.substring(cookieName.length, cookie.length);
    }
  }
  return null;
};

export const deleteCookie = (name) => {
  document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;SameSite=Strict`;
};

// Специальные функции для работы с токенами
export const setAuthTokens = (accessToken, refreshToken) => {
  // Access token на 30 минут
  setCookie('authToken', accessToken, 30);
  // Refresh token на 1 день
  setCookie('refreshToken', refreshToken, 24 * 60);
};

export const getAuthToken = () => getCookie('authToken');
export const getRefreshToken = () => getCookie('refreshToken');

export const clearAuthTokens = () => {
  deleteCookie('authToken');
  deleteCookie('refreshToken');
};

// Универсальная функция для получения текста ошибки
export function getErrorMessage(error, fallback = 'Произошла ошибка') {
  // Если есть detail
  if (error?.response?.data?.detail) return error.response.data.detail;
  // Если есть message
  if (error?.response?.data?.message) return error.response.data.message;
  // Если это строка (например, HTML)
  if (typeof error?.response?.data === 'string') {
    // Если это HTML-страница ошибки
    if (error.response.data.trim().startsWith('<!DOCTYPE html>')) {
      return fallback;
    }
    return error.response.data;
  }
  // Если это объект (например, словарь с ошибками)
  if (error?.response?.data && typeof error.response.data === 'object') {
    // Пробуем собрать все сообщения в одну строку
    return Object.values(error.response.data).flat().join(' ') || fallback;
  }
  if (error instanceof Error) return error.message;
  if (typeof error === 'string') return error;
  return fallback;
} 