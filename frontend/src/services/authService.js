import api from '../api/axios' // Ваш настроенный axios instance

// Авторизация (логин)
export async function login(username, password) {
  try {
    // console.log('VITE_API_BASE_URL:', import.meta.env.VITE_API_BASE_URL);
    const response = await api.post('/auth/jwt/create/', { username, password })
    console.log('Успешная авторизация')
    return response.data
  } catch (error) {
    // console.log('VITE_API_BASE_URL:', import.meta.env.VITE_API_BASE_URL);
    throw error.response?.data || error.message
  }
}

// Обновление токена
export async function refreshToken() {
  try {
    const refresh = localStorage.getItem('refreshToken')
    if (!refresh) throw new Error('Refresh токен отсутствует')

    const response = await api.post('/auth/jwt/refresh/', { refresh })
    localStorage.setItem('authToken', response.data.access)
    return response.data.access
  } catch (error) {
    throw error.response?.data || error.message
  }
}

// Выход (logout)
export async function logout() {
  try {
    //await api.post('/auth/jwt/logout/')
    localStorage.removeItem('authToken')
    localStorage.removeItem('refreshToken')
    window.location.href = '/auth' // Перенаправление на страницу авторизации
  } catch (error) {
    console.error('Ошибка при выходе:', error)
  }
}

// Проверка токена
export async function verifyToken(token) {
  try {
    await api.post('/auth/jwt/verify/', { token })
    return true
  } catch {
    return false
  }
}
