import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ProductListPage from '../views/ProductListPage.vue'
import BasketPage from '../views/BasketPage.vue'
import ProductPage from '../views/ProductPage.vue'
import AuthPage from '../views/AuthPage.vue'
import CheckoutPage from '../views/CheckoutPage.vue'
import { getAuthToken } from '@/utils/cookies'

const routes = [
  {
    path: '/auth',
    name: 'Auth',
    component: AuthPage,
    props: (route) => ({
      mode: route.query.mode || 'login',
      uid: route.query.uid || null,
      token: route.query.token || null,
    }),
    meta: { requiresAuth: false },
  },
  {
    path: '/auth/activate/:uid/:token',
    name: 'AccountActivation',
    component: AuthPage,
    props: (route) => ({
      mode: 'activateAccount',
      uid: route.params.uid,
      token: route.params.token,
    }),
    meta: { requiresAuth: false },
  },
  {
    path: '/auth/password/reset/:uid/:token',
    name: 'PasswordReset',
    component: AuthPage,
    props: (route) => ({
      mode: 'resetPassword',
      uid: route.params.uid,
      token: route.params.token,
    }),
    meta: { requiresAuth: false },
  },
  {
    path: '/auth/username/reset/:uid/:token',
    name: 'UsernameReset',
    component: AuthPage,
    props: (route) => ({
      mode: 'resetUsername',
      uid: route.params.uid,
      token: route.params.token,
    }),
    meta: { requiresAuth: false },
  },
  {
    path: '/auth/email/reset/:uid/:token',
    name: 'EmailReset',
    component: AuthPage,
    props: (route) => ({
      mode: 'resetEmail',
      uid: route.params.uid,
      token: route.params.token,
    }),
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    name: 'home',
    component: ProductListPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/basket',
    name: 'basket',
    component: BasketPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/product/:id',
    name: 'product',
    component: ProductPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/checkout',
    name: 'Checkout',
    component: CheckoutPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/orders',
    name: 'Orders',
    component: () => import('@/views/OrdersPage.vue'),
    meta: {
      requiresAuth: true,
      title: 'Мои заказы'
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/ProfilePage.vue'),
    meta: {
      requiresAuth: true,
      title: 'Личный кабинет'
    }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || '/'),
  routes,
})

// Сохраняем текущий маршрут перед редиректом
let savedRoute = null;

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  const token = getAuthToken()

  // Если переходим на страницу авторизации и уже авторизованы
  if (to.path.startsWith('/auth') && token && authStore.isAuthenticated) {
    // Если есть сохраненный маршрут, переходим по нему
    if (savedRoute && savedRoute.path !== '/auth') {
      const route = savedRoute
      savedRoute = null
      return next(route)
    }
    return next('/')
  }

  // Если страница требует авторизации
  if (to.meta.requiresAuth) {
    try {
      // Проверяем токен
      if (!token) {
        savedRoute = to
        return next('/auth')
      }

      // Проверяем валидность токена
      const isValid = await authStore.verifyAuthToken()
      if (!isValid) {
        // Пробуем обновить токен
        try {
          await authStore.refreshAuthToken()
          return next()
        } catch {
          savedRoute = to
          return next('/auth')
        }
      }

      return next()
    } catch (error) {
      console.error('Ошибка при проверке авторизации:', error)
      savedRoute = to
      return next('/auth')
    }
  }

  next()
})

// Очистка сохраненного маршрута при успешном входе
router.afterEach((to) => {
  if (to.path === '/') {
    savedRoute = null
  }
})

export default router
