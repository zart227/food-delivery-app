<template>
  <header class="header">
    <div
:class="{
      'container header__wrapper': true,
      'container__secandary': smallContainer
    }">
      <div v-if="isBasket" class="header__back">
        <router-link to="/">
          <ButtonComponent font-icon='fa-solid fa-arrow-left fa-2xs' is-basket-card icon-show />
        </router-link>
      </div>
      <ButtonComponent v-if="isItem" font-icon='fa-solid fa-arrow-left fa-2xs' is-basket-card icon-show @click="router.go(-1)" />
      <h1 class="header__title"> {{ title }} </h1>

      <div class="header__info">

        <div v-if="!isBasket" class="header__basket">
          <p class="header__link">{{ basketCount.length }} товара<br>на сумму {{ (basketCount.reduce((a, b) => a + b.price, 0)).toLocaleString() }} ₽</p>

          <router-link to="/Basket">
            <ButtonComponent font-icon='fa-solid fa-regular fa-basket-shopping fa-3xs' is-basket-main icon-show />
          </router-link>

        </div>

        <ButtonComponent is-basket-footer text-show button-text="Выйти" @click="logout" />
      </div>
    </div>
  </header>
</template>

<script>
//  import { ref } from 'vue'
import { computed } from 'vue'
import { useBasketStore } from '@/stores/basket'
import { useRouter } from 'vue-router'

// import basketIcon from '@/components/icons/basketIcon.vue'
import ButtonComponent from '@/components/ui/ButtonComponent.vue'
// import ButtonGoOut from '@/components/ui/ButtonGoOut.vue'

export default {
  name: 'HeaderComponent',
  components: {
    // basketIcon,
    ButtonComponent
    // ButtonGoOut
  },
  props: {
    title: {
      type: String,
      default: ''
    },
    isBasket: {
      type: Boolean,
      default: false
    },
    smallContainer: {
      type: Boolean,
      default: false
    },
    isItem: {
      type: Boolean,
      default: false
    }
  },
  setup () {
    const basketStore = useBasketStore()

    const router = useRouter()

    const basketCount = computed(() => basketStore.getBasketGoods)

    return {
      // count,
      // price,
      router,
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
  background-color: #161516;
  color: #fff;
  padding: 48px 0 75px 0;

  &__wrapper {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  &__info {
    display: flex;
    align-items: center;
    gap: 0 20px;
  }

  &__basket {
    display: flex;
    align-items: center;
    gap: 0 20px;
  }

  &__title {
    font-size: 31px;
    font-family: Montserrat;
    font-weight: 700;
  }

  &__link {
    // display: flex;
    // justify-content: space-between;
    // align-items: center;
    font-size: 17px;
    font-family: Montserrat;
    font-weight: 500;
  }

  // :deep(.button) {

  //   border: 1px solid #D58C51;
  //   color: #D58C51;

  //   &:hover {
  //     color: inherit;

  //   }
  // }

}
</style>
