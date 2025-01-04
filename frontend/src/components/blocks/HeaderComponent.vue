<template>
  <div :class="['header', headerClass]">
    <div class="header__left_block">
      <!-- Кнопка "Назад" отображается только на странице корзины -->
      <router-link :to="backRoute">
        <ButtonComponent
          v-if="showBackButton"
          font-icon="fa-solid fa-arrow-left fa-2xs"
          is-basket-card
          icon-show
        />
      </router-link>
      
      <ButtonComponent v-if="isProduct" font-icon='fa-solid fa-arrow-left fa-2xs' is-basket-card icon-show @click="router.go(-1)" />

      <p class="header__name">{{ title }}</p>
    </div>

    <!-- Информация о корзине отображается только на главной странице -->
    <div class="header__right_block">
      <div v-if="showCartInfo" class="header__cart_info">
        <div class="header__cart_info_text">
          <p>{{ countBasket + ' ' + textBasketCount }}</p>
          <p>{{ 'на сумму ' + sumBasket.toLocaleString() + ' ₽' }}</p>
        </div>
        <router-link to="/basket">
          <ButtonComponent
            font-icon="fa-solid fa-regular fa-basket-shopping fa-3xs"
            is-basket-main
            icon-show
          />
        </router-link>
      </div>
      <ButtonComponent
        is-basket-footer
        text-show
        button-text="Выйти"
        @click="handleLogout"
      />
    </div>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import ButtonComponent from '../ui/ButtonComponent.vue'
import { useBasketStore } from '@/stores/basket'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'


export default {
  name: 'HeaderComponent',
  components: {
    ButtonComponent,
  },
  props: {
    title: {
      type: String,
      default: '', // Текст заголовка
    },
    showBackButton: {
      type: Boolean,
      default: false, // Отображать ли кнопку "Назад"
    },
    backRoute: {
      type: String,
      default: '/', // Маршрут для кнопки "Назад"
    },
    isProduct: {
      type: Boolean,
      default: false
    },
    isMain: {
      type: Boolean,
      default: false
    },
    isBasketCart: {
      type: Boolean,
      default: false
    },
    showCartInfo: {
      type: Boolean,
      default: false
    },
    
  },
  setup() {
    const store = useBasketStore()
    const authStore = useAuthStore()
    const router = useRouter()
    const toast = useToast()

    // Загрузка корзины при монтировании компонента
    onMounted(async () => {
      if (authStore.isAuthenticated) { // Убедитесь, что пользователь авторизован
        await store.fetchUserBasket();
      }
    });

    // Количество товаров в корзине
    const countBasket = computed(() => store.getCountProductsInBasket)

    // Общая стоимость товаров в корзине
    const sumBasket = computed(() => store.getAllPriceProductsInBasket)

    // Текст после количества товаров
    const textBasketCount = computed(() => {
      if (countBasket.value > 10 && countBasket.value < 20) return 'товаров'
      if (countBasket.value % 10 == 1) return 'товар'
      if ([2, 3, 4].includes(countBasket.value % 10)) return 'товара'
      return 'товаров'
    })

    // Возврат на предыдущую страницу
    const goBack = () => {
      window.history.back()
    }

    // Обработчик выхода
    const handleLogout = async () => {
      try {
        await authStore.logoutUser()
      } catch (error) {
        toast.error('Произошла ошибка при выходе:', error)
        console.error('Ошибка при выходе:', error)
      }
    }

    return {
      countBasket,
      sumBasket,
      textBasketCount,
      goBack,
      handleLogout,
      router,
      toast,
    }
  },
  computed: {
    headerClass: function () {
      return {
        header__main: this.isMain,
        header__basket: this.isBasketCart,
        header__product: this.isProduct
      }
    }
  }
}
</script>

<style lang="scss" scoped>
/* Общие стили для всех типов шапки */
.header {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 40px;
  padding-top: 50px;
  color: #fff;

  .header__name {
    font-family: Montserrat;
    font-size: 31px;
    font-weight: 700;
    line-height: normal;
    text-transform: uppercase;
  }
}

/* Стили для главной страницы */
.header__main {
  padding-left: 94px;
  padding-right: 94px;
  width: 1440px;

  .header__right_block {
    display: flex;
    gap: 34px;
  }

  .header__cart_info {  
    display: flex;
    gap:20px;
  }
  
  .header__cart_info_text {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 5px;
    text-align: right;
    font-family: Montserrat;
    font-size: 17px;
    font-weight: 500;

    p {
      display: block;
    }
  }
}

/* Стили для корзины */
.header__basket {
  display: flex;
  justify-content: space-around;
  // align-items: center;

  .header__left_block {
    display: flex;
    justify-content: space-between;
    flex-direction: row;
    align-items: center;
    gap: 50px;
  }

  .header__name {
    color: #fff;
    font-family: Montserrat;
    font-size: 31px;
    font-style: normal;
    font-weight: 700;
    line-height: normal;
    text-transform: uppercase;
  }

}
.header__product {
  padding-left: 94px;
  padding-right: 94px;
  width: 1440px;

  .header__right_block {
    display: flex;
    gap: 34px;
  }

  .header__cart_info {  
    display: flex;
    gap:20px;
  }
  
  .header__cart_info_text {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 5px;
    text-align: right;
    font-family: Montserrat;
    font-size: 17px;
    font-weight: 500;

    p {
      display: block;
    }
  }
}
</style>
