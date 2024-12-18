<template>
  <div class="main">
      <div class="main__info">
        <!-- вывод общей стоимости товаров в корзине   -->
        <span class="main__info-price">{{ (basketCount.reduce((a, b) => a + b.price, 0)).toLocaleString()  }} ₽</span>
          <p class="main__info-text">Заказ на сумму:</p>
      </div>
      <ButtonComponent is-basket-footer text-show button-text="Оформить заказ" />
  </div>
</template>

<script>
// import { ref } from 'vue'
import ButtonComponent from '../ui/ButtonComponent.vue'
//import { useStore } from 'vuex'
import { useBasketStore } from '@/stores/basket'
import { computed } from 'vue'
export default {
  name: 'FooterBasket',
  components: {
    ButtonComponent
  },
  props: {
    price: {
      type: Number,
      default: 0
    }
  },
  setup () {
    const basketStore = useBasketStore() // Получение объекта хранилища

    const basketCount = computed(() => basketStore.getBasketGoods) // получение данных о товарах в корзине из геттера хранилища
    
    return {
      basketCount
    }
  }
}
</script>

<style lang="scss" scoped>
.main {
    display: flex;
    flex-direction: row;
    align-content: flex-end;
    align-items: center;
    justify-content: center;
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
