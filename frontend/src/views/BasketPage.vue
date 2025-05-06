<template>
  <div class="main container__secondary">
    <div class="main__header">
      <!-- <HeaderBasket /> -->
      <HeaderComponent
        title="Корзина с выбранными товарами"
        is-basket-cart
        show-back-button
        back-route="/"        
      />
    </div>
    <div class="main__goods">
      <MainBasket />
    </div>
    <hr class="separator" />
    <div class="main__footer">
      <FooterBasket />
    </div>
  </div>
</template>

<script>
// import { ref } from 'vue'
// import HeaderBasket from '@/components/blocks/HeaderBasket.vue'
import HeaderComponent from '../components/blocks/HeaderComponent.vue'
import MainBasket from '@/components/blocks/MainBasket.vue'
import FooterBasket from '@/components/blocks/FooterBasket.vue'
import { onBeforeMount } from 'vue'
import { useBasketStore } from '@/stores/basket'
import { useToast } from 'vue-toastification'
import { getErrorMessage } from '@/utils/cookies'

export default {
  name: 'BasketPage',
  components: {
    HeaderComponent,
    MainBasket,
    FooterBasket,
  },
  props: {},
  setup() {
    const basketStore = useBasketStore()
    const toast = useToast()

    onBeforeMount(async () => {
      try {
        await basketStore.fetchUserBasket()
      } catch (error) {
        const message = getErrorMessage(error, 'Произошла ошибка загрузки корзины!')
        toast.error(message)
        console.error('Ошибка загрузки корзины:', error)
      }
    })
  },
}
</script>

<style lang="scss" scoped>
.main__header {
  padding-top: 54px;
  padding-bottom: 81px;
}

.main__footer {
  width: 100%;
  // position: fixed;
  height: 20%;
  bottom: 0;
  left: 0;
}

.separator {
  margin-top: 100px;
  margin-bottom: 28px;
  border: 1px solid rgb(213, 140, 81);
}
</style>
