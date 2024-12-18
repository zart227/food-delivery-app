<template>
  <router-view />
</template>

<script setup>
import { onBeforeMount } from 'vue'
import { useBasketStore } from '@/stores/basket'

// Используем Pinia-хранилище корзины
const basketStore = useBasketStore()

onBeforeMount(() => {
  // Проверяем наличие данных корзины в localStorage
  if (!localStorage.getItem('basket')) {
    localStorage.setItem('basket', JSON.stringify([]))
  } else {
    // Загружаем данные корзины из localStorage в Pinia-хранилище
    basketStore.setStoreBasket()
  }
})
</script>

<style lang="scss">
* {
  margin: 0;
  padding: 0;
}
</style>
