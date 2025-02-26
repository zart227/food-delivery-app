import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth';
import ProductListPage from '../views/ProductListPage.vue'
import BasketPage from '../views/BasketPage.vue'
import ProductPage from '../views/ProductPage.vue'
import AuthPage from '../views/AuthPage.vue'
import CheckoutPage from '../views/CheckoutPage.vue'


const routes = [
  {
    path: '/auth',
    name: 'Auth',
    component: AuthPage,
    props: (route) => ({
      mode: route.query.mode || 'login', // Устанавливаем режим из параметра query или по умолчанию 'login'
      uid: route.query.uid || null,
      token: route.query.token || null,
    }),
  },
  {
    path: '/',
    name: 'home',
    component: ProductListPage,
    meta: { requiresAuth: true }, // Требуется аутентификация для доступа к этому маршруту
  },
  {
    path: '/basket',
    name: 'basket',
    component: BasketPage,
    meta: { requiresAuth: true }, // Требуется аутентификация для доступа к этому маршруту
  },
  {
    path: '/product/:id',
    name: 'product',
    component: ProductPage,
    meta: { requiresAuth: true }, // Требуется аутентификация для доступа к этому маршруту
  },
  {
    path: '/checkout',
    name: 'Checkout',
    component: CheckoutPage,
  },
  {
    path: '/orders',
    name: 'Orders',
    component: () => import('@/views/OrdersPage.vue'),
    meta: {
      requiresAuth: true,
      title: 'Мои заказы'
    }
  }
]

// создает экземпляр маршрутизатора, который определяет, какие компоненты должны быть отображены
// при изменении URL-адреса веб-приложения
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || '/'),
  routes,
})

// Глобальная навигационная охрана для проверки аутентификации
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    const isValid = await authStore.verifyAuthToken();
    if (!isValid) {
      next('/auth');
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router
