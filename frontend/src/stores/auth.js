import { defineStore } from 'pinia'
import {
  login,
  refreshToken,
  verifyToken,
  getCurrentToken
} from '../services/authService'
import router from '../router'
import api from '../api/axios'
import { getAuthToken, clearAuthTokens, setAuthTokens } from '../utils/cookies'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: !!getAuthToken(),
    user: null,
  }),

  actions: {
    async loginUser(username, password) {
      try {
        const data = await login(username, password)
        this.isAuthenticated = true
        await this.loadCurrentUser()
      } catch (error) {
        this.isAuthenticated = false
        throw error
      }
    },

    async loadCurrentUser() {
      try {
        const response = await api.get('/auth/users/me/')
        this.user = response.data
      } catch (error) {
        console.error('Ошибка при загрузке данных пользователя:', error)
        await this.logoutUser()
        throw error
      }
    },

    async refreshAuthToken() {
      try {
        const newToken = await refreshToken()
        this.isAuthenticated = true
        return newToken
      } catch (error) {
        console.error('Ошибка обновления токена:', error)
        await this.logoutUser()
        throw error
      }
    },

    async logoutUser() {
      this.isAuthenticated = false
      this.user = null
      clearAuthTokens()
      
      if (router.currentRoute.value.meta.requiresAuth) {
        await router.push('/auth')
      }
    },

    async verifyAuthToken() {
      const token = getCurrentToken()
      if (!token) {
        this.isAuthenticated = false
        return false
      }

      try {
        const isValid = await verifyToken(token)
        this.isAuthenticated = isValid
        return isValid
      } catch (error) {
        console.error('Ошибка проверки токена:', error)
        await this.logoutUser()
        return false
      }
    },

    async checkAuthStatus() {
      const token = getCurrentToken()
      if (!token) {
        await this.logoutUser()
        return false
      }

      try {
        const isValid = await this.verifyAuthToken()
        if (isValid) {
          await this.loadCurrentUser()
          return true
        }
        return false
      } catch (error) {
        console.error('Ошибка проверки статуса авторизации:', error)
        await this.logoutUser()
        return false
      }
    },
  },
})
