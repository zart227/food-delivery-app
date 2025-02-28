import api from '../api/axios' // Ваш настроенный axios instance
import router from '../router' // Импортируем router
import { setAuthTokens, getAuthToken, getRefreshToken, clearAuthTokens } from '../utils/cookies'

// Авторизация (логин)
export async function login(username, password) {
  try {
    // console.log('VITE_API_BASE_URL:', import.meta.env.VITE_API_BASE_URL);
    const response = await api.post('/auth/jwt/create/', { username, password })
    console.log('Успешная авторизация')
    const { access, refresh } = response.data
    setAuthTokens(access, refresh)
    return response.data
  } catch (error) {
    // console.log('VITE_API_BASE_URL:', import.meta.env.VITE_API_BASE_URL);
    throw error.response?.data || error.message
  }
}

// Обновление токена
export async function refreshToken() {
  try {
    const refresh = getRefreshToken()
    if (!refresh) throw new Error('Refresh токен отсутствует')

    const response = await api.post('/auth/jwt/refresh/', { refresh })
    const { access } = response.data
    setAuthTokens(access, refresh) // Обновляем только access token
    return access
  } catch (error) {
    clearAuthTokens()
    throw error.response?.data || error.message
  }
}

// Выход (logout)
export async function logout() {
  try {
    //await api.post('/auth/jwt/logout/')
    clearAuthTokens()
    await router.push('/auth') // Используем Vue Router для навигации
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

// Получение текущего токена
export function getCurrentToken() {
  return getAuthToken()
}
