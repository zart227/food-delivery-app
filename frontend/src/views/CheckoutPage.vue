<template>
  <div class="order-page">
    <HeaderComponent
      title="Оформление заказа"
      is-basket-cart
      show-back-button
      back-route="/basket"
    />
    <div class="order-page__container">
      <h2 class="order-page__title">Детали оплаты</h2>
      <form class="order-page__form" @submit.prevent="submitOrder">
        <!-- Детали оплаты -->
        <div class="order-page__section">
          <div class="order-page__form-group">
            <label for="name">Ваше ФИО *</label>
            <input id="name" v-model="orderDetails.name" required />
          </div>
          <div class="order-page__form-group">
            <label for="email">Email-адрес *</label>
            <input
              id="email"
              v-model="orderDetails.email"
              type="email"
              required
            />
          </div>
          <div class="order-page__form-group">
            <label for="phone">Телефон *</label>
            <input
              id="phone"
              v-model="orderDetails.phone"
              type="tel"
              required
            />
          </div>
          <div class="order-page__form-group">
            <label for="address">Адрес *</label>
            <input id="address" v-model="orderDetails.address" required />
          </div>
        </div>

        <!-- Дополнительная информация -->
        <h2 class="order-page__title">Дополнительная информация</h2>
        <div class="order-page__form-group">
          <label for="notes">Примечание к заказу</label>
          <textarea
            id="notes"
            v-model="orderDetails.notes"
            class="order-page__textarea"
          ></textarea>
        </div>

        <!-- Отображение заказа -->
        <div class="order-summary">
          <h2 class="order-summary__title">Ваш заказ</h2>
          <div class="order-summary__items">
            <div
              v-for="item in cartItems"
              :key="item.id"
              class="order-summary__item"
            >
              <div>{{ item.product_data.title }} × {{ item.quantity }}</div>
              <div
                >{{
                  (item.quantity * item.product_data.price).toLocaleString()
                }}
                ₽</div
              >
            </div>
          </div>
          <div class="order-summary__total">
            <span>Итого:</span>
            <span>{{ totalPrice.toLocaleString() }} ₽</span>
          </div>
        </div>

        <!-- Подтверждение заказа -->
        <button type="submit" class="order-page__button">
          Подтвердить заказ
        </button>
        <p v-if="errorMessage" class="order-page__error">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import HeaderComponent from '@/components/blocks/HeaderComponent.vue'
import { computed } from 'vue'
import { useBasketStore } from '@/stores/basket'
import { createOrder } from '@/services/orderService'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

export default {
  components: {
    HeaderComponent,
  },
  setup() {
    const basketStore = useBasketStore()
    const router = useRouter()
    const toast = useToast()

    // Данные товаров в корзине
    const cartItems = computed(() => basketStore.getBasketGoods)

    // Общая стоимость
    const totalPrice = computed(() =>
      cartItems.value.reduce(
        (total, item) => total + item.quantity * item.product_data.price,
        0,
      ),
    )

    return {
      cartItems,
      totalPrice,
      basketStore,
      router,
      toast,
    }
  },
  data() {
    return {
      orderDetails: {
        name: '',
        email: '',
        phone: '',
        address: '',
        notes: '',
      },
      errorMessage: '',
    }
  },

  methods: {
    async submitOrder() {
      try {
        // Отправка данных на сервер
        const orderData = {
          ...this.orderDetails,
          items: this.cartItems.map((item) => ({
            product: item.product_data.id,
            quantity: item.quantity,
            price: item.product_data.price,
          })),
          total_price: this.totalPrice,
        }
        await createOrder(orderData)

        // Уведомление об успешном оформлении
        this.toast.success('Ваш заказ успешно оформлен!')

        // Очистка корзины
        this.basketStore.setBasket([])

        // Переход на главную страницу
        this.router.push('/')
      } catch (error) {
        this.errorMessage = 'Не удалось оформить заказ. Попробуйте снова.'
        console.error('Ошибка оформления заказа:', error)
        this.toast.error('Ошибка оформления заказа')
      }
    },
  },
}
</script>


<style lang="scss" scoped>
// .order-page {
//   background-color: #f9f9f9;
//   color: #333;
//   min-height: 100vh;
//   padding: 20px;

//   &__container {
//     max-width: 1200px;
//     margin: 0 auto;
//     display: flex;
//     gap: 20px;
//   }

//   &__form {
//     flex: 2;
//   }

//   &__section {
//     margin-bottom: 30px;
//   }

//   &__form-group {
//     margin-bottom: 15px;

//     label {
//       display: block;
//       margin-bottom: 5px;
//       font-weight: bold;
//     }

//     input,
//     textarea {
//       width: 100%;
//       padding: 10px;
//       border: 1px solid #ccc;
//       border-radius: 4px;
//     }
//   }

//   &__textarea {
//     height: 80px;
//   }

//   &__button {
//     width: 100%;
//     padding: 12px;
//     background-color: #28a745;
//     border: none;
//     color: #fff;
//     font-weight: bold;
//     border-radius: 4px;
//     cursor: pointer;
//   }

//   &__button:hover {
//     background-color: #218838;
//   }

//   &__error {
//     color: red;
//     margin-top: 10px;
//   }
// }

.order-page {
  background-color: #000; // Черный фон
  color: #fff; // Белый текст
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  //align-items: center;

  &__container {
    align-items: center;
    background-color: #1c1c1c; // Темный контейнер
    padding: 20px 30px;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.8);
    max-width: 600px;
    width: 100%;
    margin: 20px auto;
  }

  &__title {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 15px;
    text-align: center;
    color: #f5f5f5;
  }

  &__form-group {
    margin-bottom: 15px;

    label {
      font-size: 14px;
      color: #d3d3d3;
      margin-bottom: 5px;
      display: block;
    }

    input,
    textarea {
      width: 100%;
      padding: 10px;
      border: 1px solid #555;
      border-radius: 4px;
      background-color: #333;
      color: #fff;
      font-size: 14px;
      box-sizing: border-box;

      &:focus {
        outline: none;
        border-color: #d58c51;
        box-shadow: 0 0 5px #d58c51;
      }
    }
  }

  &__textarea {
    height: 80px;
  }

  &__button {
    width: 100%;
    padding: 12px 0;
    background-color: #d58c51;
    border: none;
    color: #fff;
    font-size: 16px;
    font-weight: 600;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;

    &:hover {
      background-color: #b56f43;
    }
  }

  &__error {
    margin-top: 10px;
    color: red;
    font-size: 14px;
  }
}

.order-summary {
  flex: 1;
  // background-color: #fff;
  // border: 1px solid #ddd;
  // padding: 20px;
  // border-radius: 8px;
  padding: 20px 30px;
  // border-radius: 8px;
  border: 1px solid #555;
  border-radius: 4px;
  background-color: #333;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.8);
  max-width: 600px;
  width: 100%;
  margin: 20px auto;
  box-sizing: border-box;
  //color: #000;


  &__title {
    font-weight: bold;
    margin-bottom: 15px;
  }

  &__items {
    margin-bottom: 15px;


    &__item {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
  }

  &__item {
      display: flex;
      // flex-direction: column;
      justify-content: space-between;
      margin-bottom: 10px;
    }

  &__total {
    font-weight: bold;
    display: flex;
    justify-content: space-between;
  }
}
</style>
