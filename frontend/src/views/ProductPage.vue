<template>
  <div class="wrapper">
    <!-- <HeaderProduct is-item title="" /> -->
    <div class="header__wrapper">
      <HeaderComponent is-product show-cart-info />
    </div>

    <!-- Контент страницы -->
    <div v-if="product" class="container item">
      <div class="item__img">
        <img class="item__ipreview" :src="product.image" alt="" />
      </div>
      <div class="item__descr">
        <h2 class="item__title">{{ product.title }}</h2>
        <p class="item__description">{{ product.description }}</p>
        <div class="item__footer">
          <span class="item__price"
            >{{ product.price.toLocaleString() }} ₽</span
          >
          <ButtonComponent
            is-good-footer
            text-show
            button-text="В корзину"
            @click="addToCart"
          />
        </div>
      </div>
    </div>
    <div v-else>
      <p>Загрузка продукта...</p>
    </div>
  </div>
</template>

<script>
import { onBeforeMount, computed } from 'vue'
// import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useProductsStore } from '@/stores/products'
import { useBasketStore } from '@/stores/basket'
// import HeaderProduct from '@/components/blocks/HeaderProduct.vue'
import HeaderComponent from '@/components/blocks/HeaderComponent.vue'
import ButtonComponent from '@/components/ui/ButtonComponent.vue'
import { useToast } from 'vue-toastification'
import { getErrorMessage } from '@/utils/cookies'

export default {
  name: 'ProductPage',
  components: {
    ButtonComponent,
    // HeaderProduct,
    HeaderComponent,
    // FwbToast,
  },
  setup() {
    const route = useRoute()
    const productsStore = useProductsStore()
    const basketStore = useBasketStore()
    const toast = useToast()

    const product = computed(() => productsStore.getProductItem)

    // Состояние для уведомления
    // const alertMessage = ref('')
    // const showAlert = ref(false)

    onBeforeMount(async () => {
      if (!productsStore.getProductList.length) {
        try {
          await productsStore.fetchAllProducts() // Загрузка продуктов, если их ещё нет
        } catch (error) {
          const message = getErrorMessage(error, 'Ошибка загрузки списка продуктов!')
          console.error('Ошибка загрузки списка продуктов:', error)
          toast.error(message)
        }
      }
      productsStore.setProductItem(route.params.id) // Устанавливаем текущий продукт
    })
    const addToCart = async () => {
      if (product.value) {
        try {
          await basketStore.addGoodInBasket(product.value.id)
          toast.success('Товар добавлен в корзину!')
        } catch (error) {
          const message = getErrorMessage(error, 'Ошибка добавления товара в корзину!')
          toast.error(message)
          console.error('Ошибка добавления товара в корзину:', error)
        }
      }
    }

    return {
      product,
      addToCart,
      // alertMessage,
      // showAlert,
    }
  },
}
</script>

<style lang="scss" scoped>
.wrapper {
  background-image: url(../assets/img/bgItem.png);
  background-size: cover;
  // background-position: center;
  background-repeat: no-repeat;
  height: 100vh;
  color: #fff;
}

.header__wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

// :deep(.header) {
//   background-color: transparent;
//   // max-width: 1304px;
// }

.item {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  overflow: auto;

  &__ipreview {
    width: 501px;
    height: 503px;
  }

  &__descr {
    padding: 60px 10px 40px 150px;
  }

  &__title {
    font-size: 30px;
    font-family: Montserrat;
    font-weight: 500;
    margin-bottom: 46px;
    color: #d58c51;
  }

  &__description {
    font-size: 14px;
    font-family: Montserrat;
    font-weight: 400;
    margin-bottom: 30px;
  }

  &__price {
    font-size: 23px;
    font-family: Montserrat;
    font-weight: 500;
    padding-right: 137px;
  }

  &__footer {
    display: flex;
    align-items: center;
    // justify-content: space-between;
    margin-top: 34px;
    margin-bottom: 30px;
  }
}
</style>
