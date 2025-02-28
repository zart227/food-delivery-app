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