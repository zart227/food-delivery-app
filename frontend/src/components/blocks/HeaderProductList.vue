<template>
  <div class="header">
    <h1 class="header__title">наша продукция</h1>
    <div class="header__cart">
      <div class="header__text">
        <span>{{ basketCount.length }} товара</span>
        <!-- сумма стоимости всех товаров в корзине -->
        <span>на сумму {{ (basketCount.reduce((a, b) => a + b.price, 0)).toLocaleString()  }} ₽</span>
      </div>
      <router-link to="/basket">
        <ButtonComponent font-icon='fa-solid fa-regular fa-basket-shopping fa-3xs' is-basket-main icon-show />
      </router-link>
      <ButtonComponent is-basket-footer text-show button-text="Выйти" @click="logout" />
    </div>
  </div>
</template>

<script>
// import { ref } from 'vue'
import { useBasketStore } from '@/stores/basket'
import { computed } from 'vue'
import ButtonComponent from '../ui/ButtonComponent.vue'
export default {
  name: 'HeaderProductList',
  components: {
    ButtonComponent
  },
  props: {
  },
  setup () {
    const basketStore = useBasketStore()

    const basketCount = computed(() => basketStore.getBasketGoods)

    return {
      basketCount
    }
  },
  methods: {
    logout () {
      // Очищаем локальное хранилище и перенаправляем на страницу авторизации
      localStorage.setItem('currentUser', [])
      localStorage.setItem('isAuthenticated', false)
      this.$router.push('/auth')
    }
  }
}
</script>

<style lang="scss" scoped>
.header {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
}

.header__title {
  color: #FFF;
  font-family: Montserrat;
  font-size: 31px;
  font-style: normal;
  font-weight: 700;
  line-height: normal;
  text-transform: uppercase;
}

.header__text {
  color: #FFF;
  text-align: right;
  font-family: Montserrat;
  font-size: 17px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
  display: flex;
  align-items: flex-end;
  flex-direction: column;
}

.header__cart {
  display: flex;
  flex-direction: row;
  gap: 10px;
}
</style>
