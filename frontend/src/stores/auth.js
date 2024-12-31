import { defineStore } from 'pinia'
import {
  login,
  refreshToken,
  logout,
  verifyToken,
} from '../services/authService'
import api from '../api/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    authToken: localStorage.getItem('authToken') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
    isAuthenticated: !!localStorage.getItem('authToken'),
    user: null, // Состояние для хранения текущего пользователя
  }),

  actions: {
    async loginUser(username, password) {
      try {
        const data = await login(username, password)
        this.authToken = data.access
        this.refreshToken = data.refresh
        this.isAuthenticated = true

        // // Сохраняем токены в localStorage
        localStorage.setItem('authToken', this.authToken)
        localStorage.setItem('refreshToken', this.refreshToken)

        // Загружаем данные текущего пользователя
        await this.loadCurrentUser()
      } catch (error) {
        console.error('Ошибка при авторизации:', error)
        throw error
      }
    },

    async loadCurrentUser() {
      try {
        const response = await api.get('/auth/users/me/')
        this.user = response.data
      } catch (error) {
        console.error('Ошибка при загрузке данных пользователя:', error)
        this.logoutUser()
      }
    },

    async refreshAuthToken() {
      try {
        const newToken = await refreshToken()
        this.authToken = newToken
        this.isAuthenticated = true
        // Также можно обновить текущего пользователя после обновления токена
        await this.loadCurrentUser()
      } catch (error) {
        console.error('Ошибка обновления токена:', error)
        this.logoutUser()
      }
    },

    async logoutUser() {
      try {
        await logout()
        this.authToken = null
        this.refreshToken = null
        this.isAuthenticated = false
        this.user = null
      } catch (error) {
        console.error('Ошибка при выходе:', error)
      }
    },

    async verifyAuthToken() {
      if (!this.authToken) {
        this.isAuthenticated = false
        return false
      }
      try {
        const isValid = await verifyToken(this.authToken)
        this.isAuthenticated = isValid
        return isValid
      } catch (error) {
        console.error('Ошибка проверки токена:', error)
        this.logoutUser()
        return false
      }
    },

    async checkAuthStatus() {
      if (!this.authToken) {
        this.logoutUser()
        return
      }

      try {
        await this.verifyAuthToken()
        if (this.isAuthenticated) {
          await this.loadCurrentUser()
        }
      } catch (error) {
        console.error('Ошибка проверки статуса авторизации:', error)
        this.logoutUser()
      }
    },
  },
})
