<template>
  <div class="orders-page">
    <HeaderComponent
      title="Мои заказы"
      show-back-button
      back-route="/"
    />
    
    <div class="orders-page__container">
      <div v-if="isLoading" class="orders-page__loading">
        Загрузка заказов...
      </div>

      <div v-else-if="error" class="orders-page__error">
        {{ error }}
      </div>

      <div v-else-if="!orders.length" class="orders-page__empty">
        <p>У вас пока нет заказов</p>
        <router-link to="/" class="orders-page__link">
          Перейти к покупкам
        </router-link>
      </div>

      <template v-else>
        <div class="orders-page__filters">
          <div class="orders-page__filter-group">
            <label>Статус:</label>
            <select v-model="selectedStatus">
              <option value="">Все</option>
              <option value="pending">Ожидает обработки</option>
              <option value="processing">В обработке</option>
              <option value="completed">Выполнен</option>
            </select>
          </div>

          <div class="orders-page__filter-group">
            <label>Сортировка:</label>
            <select v-model="sortOrder">
              <option value="newest">Сначала новые</option>
              <option value="oldest">Сначала старые</option>
            </select>
          </div>
        </div>

        <div class="orders-page__list">
          <OrderCard
            v-for="order in filteredAndSortedOrders"
            :key="order.id"
            :order="order"
          />
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import HeaderComponent from '@/components/blocks/HeaderComponent.vue'
import OrderCard from '@/components/blocks/OrderCard.vue'
import { useOrdersStore } from '@/stores/orders'
import { useToast } from 'vue-toastification'

export default {
  name: 'OrdersPage',
  components: {
    HeaderComponent,
    OrderCard
  },

  setup() {
    const ordersStore = useOrdersStore()
    const toast = useToast()
    const selectedStatus = ref('')
    const sortOrder = ref('newest')

    // Получаем данные из store
    const orders = computed(() => ordersStore.orders)
    const isLoading = computed(() => ordersStore.isLoading)
    const error = computed(() => ordersStore.error)

    // Фильтрация и сортировка заказов
    const filteredAndSortedOrders = computed(() => {
      let result = [...orders.value]

      // Фильтрация по статусу
      if (selectedStatus.value) {
        result = result.filter(order => order.status === selectedStatus.value)
      }

      // Сортировка
      result.sort((a, b) => {
        const dateA = new Date(a.created_at)
        const dateB = new Date(b.created_at)
        return sortOrder.value === 'newest' ? dateB - dateA : dateA - dateB
      })

      return result
    })

    // Инициализация WebSocket при монтировании
    onMounted(() => {
      ordersStore.initWebSocket()
    })

    // Отключение WebSocket при размонтировании
    onUnmounted(() => {
      ordersStore.clearOrdersData()
    })

    return {
      orders,
      isLoading,
      error,
      selectedStatus,
      sortOrder,
      filteredAndSortedOrders
    }
  }
}
</script>

<style lang="scss" scoped>
.orders-page {
  min-height: 100vh;
  background-color: #000;
  color: #fff;

  &__container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }

  &__loading,
  &__error,
  &__empty {
    text-align: center;
    padding: 40px;
    background-color: #1c1c1c;
    border-radius: 8px;
    margin-top: 20px;
  }

  &__error {
    color: #e53e3e;
  }

  &__link {
    display: inline-block;
    margin-top: 16px;
    padding: 8px 16px;
    background-color: #d58c51;
    color: #fff;
    text-decoration: none;
    border-radius: 4px;
    transition: background-color 0.3s;

    &:hover {
      background-color: #b56f43;
    }
  }

  &__filters {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
    padding: 16px;
    background-color: #1c1c1c;
    border-radius: 8px;
  }

  &__filter-group {
    display: flex;
    align-items: center;
    gap: 8px;

    label {
      color: #888;
    }

    select {
      padding: 6px 12px;
      background-color: #333;
      border: 1px solid #555;
      border-radius: 4px;
      color: #fff;
      cursor: pointer;

      &:focus {
        outline: none;
        border-color: #d58c51;
      }
    }
  }

  &__list {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
}
</style> 