<template>
  <router-view />
</template>

<script setup>
// import { onBeforeMount } from 'vue'
// import { useBasketStore } from '@/stores/basket'
// import { useAuthStore } from '@/stores/auth' // Pinia для управления авторизацией
// // import api from './api/axios'   // Настроенный axios

// const basketStore = useBasketStore()
// const authStore = useAuthStore()

// onBeforeMount(async () => {
//   try {
//     await authStore.checkAuthStatus() // Проверяем авторизацию и устанавливаем пользователя
//     if (authStore.isAuthenticated) {
//       await basketStore.fetchUserBasket() // Загружаем корзину только если пользователь авторизован
//     }
//   } catch (error) {
//     console.error('Ошибка при инициализации приложения:', error)
//   }
// })
</script>

<style lang="scss">
* {
  margin: 0;
  padding: 0;
}
</style>
