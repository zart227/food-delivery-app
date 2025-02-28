<template>
  <router-view />
</template>

<script setup>
import { onBeforeMount } from 'vue'
import { useBasketStore } from '@/stores/basket'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const basketStore = useBasketStore()
const authStore = useAuthStore()
const router = useRouter()

onBeforeMount(async () => {
  try {
    const isAuthenticated = await authStore.checkAuthStatus()
    if (isAuthenticated) {
      await basketStore.fetchUserBasket()
    } else if (router.currentRoute.value.meta.requiresAuth) {
      await router.push('/auth')
    }
  } catch (error) {
    console.error('Ошибка при инициализации приложения:', error)
    if (router.currentRoute.value.meta.requiresAuth) {
      await router.push('/auth')
    }
  }
})
</script>

<style lang="scss">
* {
  margin: 0;
  padding: 0;
}
</style>
