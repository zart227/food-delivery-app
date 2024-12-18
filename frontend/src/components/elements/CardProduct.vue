<template>
  <div
    class="card-product"
    @click="router.push(`/product/${productId}`)"
  >
    <div v-if="!line" class="card">
      <div class="card__info">

          <img class="card__image" :src="resolvedImageSource" alt="image.png">

        <h2 class="card__title">{{ title }}</h2>
        <h3 class="card__description">{{ description }}</h3>
      </div>
      <div class="card__footer">
        <div class="card__price">
          <span>{{ price.toLocaleString()  }} ₽</span>
        </div>
        <ButtonComponent
         font-icon='fa-solid fa-plus fa-2xs' is-main icon-show @click.stop="$emit('clickMain')" />
      </div>
    </div>
    <div v-else class="cardBasket">
      <div class="cardBasket__descr">
        <img class="cardBasket_image" :src="resolvedImageSource" alt="image.png">
        <h2 class="card__title">{{ title }}</h2>
      </div>
      <div class="cardBasket__elemets">
        <div class="card__price">
          <span>{{ price.toLocaleString()  }} ₽</span>
        </div>
        <ButtonComponent
         font-icon='fa-solid fa-plus fa-2xs' is-basket-card icon-show is-rotated @click.stop="$emit('clickBasket')" />
      </div>
    </div>
  </div>
</template>

<script>
// import { ref } from 'vue'
import ButtonComponent
  from '../ui/ButtonComponent.vue'
import { useRouter } from 'vue-router'

export default {
  name: 'CardProduct',
  components: {
    ButtonComponent,
  },
  props: {
    line: Boolean,
    productId: {
      type: Number,
      required: true
    },
    title: {
      type: String,
      default: 'Название блюда'
    },
    description: {
      type: String,
      default: 'Описание блюда'
    },
    price: {
      type: Number,
      default: 0
    },
    imageSource: {
      type: String,
      default: 'default'
    }
  },
  
  setup () {
    const router = useRouter()
    // const goToProductPage = () => {
    //   // Используем метод push маршрутизатора для перехода на страницу товара с нужным id
    //   router.push({ name: 'product', params: { id: this.productId } })
    // }
    return {
      // goToProductPage,
      router
    }
  },

  computed: {
    resolvedImageSource() {
      // Если imageSource — это функция (например, из import.meta.glob), вызываем её
      return typeof this.imageSource === 'function' ? this.imageSource() : this.imageSource
    }
  }
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
  border: 1px solid #D58C51;
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
  width: 860px;
}

.card__image {
  width: 270px;
  height: 271px;
  flex-shrink: 0;
  padding-bottom: 30px;
  ;
}

.card__info {
  display: flex;
  flex-direction: column;
  padding: 20px 20px;
  gap: 13px
}

.card__footer {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 169px;
  padding-bottom: 36px
}

.card__title {
  color: #FFF;
  font-family: Montserrat;
  font-size: 17px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
}

.card__description {
  color: #FFF;
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

.cardBasket__elemets {
  display: flex;
  align-items: center;
  gap: 21px;
}

.cardBasket_image {
  // position: absolute;
  width: 132px;
}

.cardBasket__descr {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 88px;
}

.card:hover .card__title {
  color: #D58C51;
}

 //При наведении курсора карточка сместится на 20 пикселей
.card:hover {
  transform: translate(0%, -20px);;
}
.card:hover .card__description {
  color: #D58C51;
}

</style>
