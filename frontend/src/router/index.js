import { createRouter, createWebHistory } from 'vue-router'
import ProductListPage from '../views/ProductListPage.vue'
import BasketPage from '../views/BasketPage.vue'
import ProductPage from '../views/ProductPage.vue'
import Auth from '../views/AuthPage.vue'

const routes = [
  {
    path: '/auth',
    name: 'Auth',
    component: Auth
  },
  {
    path: '/',
    name: 'home',
    component: ProductListPage,
    meta: { requiresAuth: true } // Требуется аутентификация для доступа к этому маршруту
  },
  {
    path: '/basket',
    name: 'basket',
    component: BasketPage,
    meta: { requiresAuth: true } // Требуется аутентификация для доступа к этому маршруту
  },
  {
    path: '/product/:id',
    name: 'product',
    component: ProductPage,
    meta: { requiresAuth: true } // Требуется аутентификация для доступа к этому маршруту
  }
]

// создает экземпляр маршрутизатора, который определяет, какие компоненты должны быть отображены
// при изменении URL-адреса веб-приложения
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || '/'),
  routes
})

// Глобальная навигационная охрана для проверки аутентификации
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated')
  // Проверяем, требует ли маршрут аутентификации и аутентифицирован ли пользователь
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Если аутентификация требуется и пользователь не аутентифицирован, перенаправляем на страницу входа
    next('/auth')
  } else {
    // Если маршрут не требует аутентификации, разрешаем доступ
    next()
  }
})

export default router
