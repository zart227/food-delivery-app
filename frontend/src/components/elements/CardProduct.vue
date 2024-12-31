<template>
  <div class="card-product" @click="router.push(`/product/${productId}`)">
    <div v-if="!line" class="card">
      <div class="card__info">
        <img class="card__image" :src="imageSource" alt="image.png" />

        <h2 class="card__title">{{ title }}</h2>
        <h3 class="card__description">{{ description }}</h3>
      </div>

      <div class="card__footer">
        <div class="card__price">
          <span>{{ price.toLocaleString() }} ₽</span>
        </div>
        <ButtonComponent
          font-icon="fa-solid fa-plus fa-2xs"
          is-main
          icon-show
          @click.stop="$emit('clickMain')"
        />
      </div>
    </div>
    <div v-else class="cardBasket">
      <div class="cardBasket__descr">
        <img class="cardBasket_image" :src="imageSource" alt="image.png" />
        <h2 class="card__title">{{ title }}</h2>
      </div>

      <div class="cardBasket__container">
        <div class="cardBasket__elements">
          
          
          <!-- Контролы количества -->
          <div class="quantity-controls">
            <button @click.stop="decreaseQuantity">-</button>
            <input
              v-model.number="localQuantity"
              type="number"
              @change="updateQuantity"
              @click.stop
            />
            <button @click.stop="increaseQuantity">+</button>
          </div>

          <div class="card__price">
            <span>{{ price.toLocaleString() }} ₽</span>
          </div>
          <ButtonComponent
            font-icon="fa-solid fa-plus fa-2xs"
            is-basket-card
            icon-show
            is-rotated
            @click.stop="$emit('clickBasket')"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { ref } from 'vue'
import ButtonComponent from '../ui/ButtonComponent.vue'
import { useRouter } from 'vue-router'
import { ref, watch } from 'vue'

export default {
  name: 'CardProduct',
  components: {
    ButtonComponent,
  },
  props: {
    line: Boolean,
    productId: {
      type: Number,
      required: true,
    },
    title: {
      type: String,
      default: 'Название блюда',
    },
    description: {
      type: String,
      default: 'Описание блюда',
    },
    price: {
      type: Number,
      default: 0,
    },
    imageSource: {
      type: String,
      default: '',
    },
    quantity: {
      type: Number,
      default: 0,
      //required: true,
    },
  },
  emits: ['updateQuantity', 'clickMain', 'clickBasket'],
  setup(props, { emit }) {
    const router = useRouter()

    // Локальное количество товара
    const localQuantity = ref(props.quantity)

    // Увеличение количества
    const increaseQuantity = () => {
      localQuantity.value += 1
      emit('updateQuantity', localQuantity.value)
    }

    // Уменьшение количества
    const decreaseQuantity = () => {
      if (localQuantity.value > 1) {
        localQuantity.value -= 1
        emit('updateQuantity', localQuantity.value)
      }
    }

    // Обновление количества через ввод
    const updateQuantity = () => {
      if (localQuantity.value < 1) {
        localQuantity.value = 1
      } else {
        localQuantity.value = Math.floor(localQuantity.value) // Только целые числа
      }
      emit('updateQuantity', localQuantity.value)
    }

    watch(() => props.quantity, (newQuantity) => {
      localQuantity.value = newQuantity
    })

    return {
      router,
      localQuantity,
      increaseQuantity,
      decreaseQuantity,
      updateQuantity,
    }
  },
}
</script>

<style lang="scss" scoped>
.card-product {
  display: flex;
  justify-content: center;
  cursor: pointer; /* Добавляем указатель при наведении, чтобы показать, что карточка кликабельна */
}

.card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #d58c51;
  width: 312px;
  flex-shrink: 0;
  animation-duration: 1s;
  transition: all 0.2s ease;
}

.cardBasket {
  display: flex;
  justify-content: space-between;
  align-content: center;
  align-items: center;
  width: 100%;
}

.card__image {
  width: 270px;
  height: 271px;
  flex-shrink: 0;
  padding-bottom: 30px;
}

.card__info {
  display: flex;
  flex-direction: column;
  padding: 20px 20px;
  gap: 13px;
}

.card__footer {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 169px;
  padding-bottom: 36px;
}

.card__title {
  color: #fff;
  font-family: Montserrat;
  font-size: 17px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
}

.card__description {
  color: #fff;
  font-family: Montserrat;
  font-size: 14px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
}

.card__price {
  color: rgb(213, 140, 81);
  font-family: Montserrat;
  font-size: 17px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
}

.cardBasket__container {
  width: 300px;
}
.cardBasket__elements {
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  gap: 21px;
  // width: 300px;
}

.cardBasket_image {
  // position: absolute;
  width: 132px;
}

.cardBasket__descr {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 40px;
}

.card:hover .card__title {
  color: #d58c51;
}

//При наведении курсора карточка сместится на 20 пикселей
.card:hover {
  transform: translate(0%, -20px);
}
.card:hover .card__description {
  color: #d58c51;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.quantity-controls button {
  background-color: #d58c51;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.quantity-controls input {
  width: 50px;
  text-align: center;
}

.quantity-controls input[type='number']::-webkit-inner-spin-button {
  position: absolute;
  width: 12.5%;
  height: 100%;
  top: 0;
  right: 0;
}
</style>
