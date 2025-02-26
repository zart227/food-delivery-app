<template>
  <div class="order-card" :class="{ 'order-card--expanded': isExpanded }">
    <div class="order-card__header" @click="toggleExpand">
      <div class="order-card__main-info">
        <h3 class="order-card__title">Заказ #{{ order.id }}</h3>
        <span class="order-card__date">{{ formatDate(order.created_at) }}</span>
      </div>
      <div class="order-card__status" :class="'order-card__status--' + order.status">
        {{ getStatusText(order.status) }}
      </div>
    </div>

    <div v-if="isExpanded" class="order-card__content">
      <div class="order-card__details">
        <div class="order-card__info-row">
          <span class="order-card__label">Адрес доставки:</span>
          <span class="order-card__value">{{ order.address }}</span>
        </div>
        <div class="order-card__info-row">
          <span class="order-card__label">Телефон:</span>
          <span class="order-card__value">{{ order.phone }}</span>
        </div>
        <div v-if="order.notes" class="order-card__info-row">
          <span class="order-card__label">Примечание:</span>
          <span class="order-card__value">{{ order.notes }}</span>
        </div>
      </div>

      <div class="order-card__items">
        <h4 class="order-card__subtitle">Состав заказа:</h4>
        <div v-for="item in order.items" :key="item.id" class="order-card__item">
          <span class="order-card__item-title">{{ item.product.title }}</span>
          <div class="order-card__item-details">
            <span>{{ item.quantity }} шт.</span>
            <span>{{ item.price.toLocaleString() }} ₽</span>
          </div>
        </div>
      </div>

      <div class="order-card__total">
        <span class="order-card__total-label">Итого:</span>
        <span class="order-card__total-value">{{ order.total_price.toLocaleString() }} ₽</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrderCard',
  props: {
    order: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      isExpanded: false
    }
  },
  methods: {
    toggleExpand() {
      this.isExpanded = !this.isExpanded
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return new Intl.DateTimeFormat('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    },
    getStatusText(status) {
      const statusMap = {
        'pending': 'Ожидает обработки',
        'processing': 'В обработке',
        'completed': 'Выполнен'
      }
      return statusMap[status] || status
    }
  }
}
</script>

<style lang="scss" scoped>
.order-card {
  background-color: #1c1c1c;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #333;

  &:hover {
    border-color: #d58c51;
  }

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  &__main-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  &__title {
    color: #fff;
    font-size: 18px;
    margin: 0;
  }

  &__date {
    color: #888;
    font-size: 14px;
  }

  &__status {
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 14px;
    font-weight: 500;

    &--pending {
      background-color: #2d3748;
      color: #cbd5e0;
    }

    &--processing {
      background-color: #2c5282;
      color: #90cdf4;
    }

    &--completed {
      background-color: #276749;
      color: #9ae6b4;
    }
  }

  &__content {
    margin-top: 20px;
    border-top: 1px solid #333;
    padding-top: 20px;
  }

  &__details {
    margin-bottom: 20px;
  }

  &__info-row {
    display: flex;
    margin-bottom: 8px;
    gap: 8px;
  }

  &__label {
    color: #888;
    min-width: 140px;
  }

  &__value {
    color: #fff;
  }

  &__items {
    margin-bottom: 20px;
  }

  &__subtitle {
    color: #d58c51;
    margin-bottom: 12px;
    font-size: 16px;
  }

  &__item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #333;

    &:last-child {
      border-bottom: none;
    }
  }

  &__item-title {
    color: #fff;
  }

  &__item-details {
    display: flex;
    gap: 16px;
    color: #888;
  }

  &__total {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px solid #333;
  }

  &__total-label {
    color: #fff;
    font-weight: 500;
  }

  &__total-value {
    color: #d58c51;
    font-size: 18px;
    font-weight: 600;
  }
}
</style> 