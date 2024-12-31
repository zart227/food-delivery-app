<template>
  <div class="main">
    <div class="main__info">
      <!-- вывод общей стоимости товаров в корзине -->
      <span class="main__info-price">
        {{ sumBasket.toLocaleString() }} ₽
      </span>
      <p class="main__info-text">Заказ на сумму:</p>
    </div>
    <ButtonComponent
      is-basket-footer
      text-show
      button-text="Оформить заказ"
      @click="navigateToCheckout"
    />
  </div>
</template>

<script>
import ButtonComponent from '../ui/ButtonComponent.vue'
import { useBasketStore } from '@/stores/basket'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'FooterBasket',
  components: {
    ButtonComponent,
  },
  props: {
    price: {
      type: Number,
      default: 0,
    },
  },
  setup() {
    const basketStore = useBasketStore() // Получение объекта хранилища
    const router = useRouter() // Инициализация Vue Router

    // Общая стоимость товаров в корзине
    // const totalPrice = computed(() =>
    //   (basketStore.getBasketGoods || []).reduce(
    //     (total, item) => total + item.quantity * item.product_data.price,
    //     0,
    //   ),
    // )

    // Количество товаров в корзине
    const countBasket = computed(() => basketStore.getCountProductsInBasket)

    // Общая стоимость товаров в корзине
    const sumBasket = computed(() => basketStore.getAllPriceProductsInBasket)

    // Переход на страницу оформления заказа
    const navigateToCheckout = () => {
      router.push('/checkout') // Переход на маршрут '/checkout'
    }

    return {
      // totalPrice,
      countBasket,
      sumBasket,
      navigateToCheckout,
    }
  },
}
</script>

<style lang="scss" scoped>
.main {
  display: flex;
  flex-direction: row;
  align-content: flex-end;
  align-items: center;
  justify-content: space-between;
  gap: 360px;
}

.main__info {
  display: flex;
  flex-direction: row-reverse;
  align-items: center;
  gap: 16px;
}

.main__info-text {
  color: rgb(255, 255, 255);
  font-family: Montserrat;
  font-size: 21px;
  font-weight: 400;
  line-height: 26px;
  letter-spacing: 0%;
  text-align: left;
  text-transform: uppercase;
}

.main__info-price {
  color: rgb(213, 140, 81);
  font-family: Montserrat;
  font-size: 18px;
  font-weight: 400;
  line-height: 22px;
  letter-spacing: 0%;
  text-align: left;
}
</style>
