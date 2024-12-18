<template>
  <div class="main">
    <CardProduct
      v-for="( cardData, index ) in prodCardData"
      :key="index"
      :product-id=cardData.id
      :title="cardData.title"
      :description="cardData.description"
      :price="cardData.price"
      :image-source="cardData.imageSource"
      @click-main = "addToBasket(cardData.id)"
    />
  </div>
</template>

<script>
// import { ref } from 'vue'
import { computed } from 'vue'
import CardProduct from '../elements/CardProduct.vue'
import { useGoodsStore } from '@/stores/goods'
import { useBasketStore } from '@/stores/basket'

export default {
  name: 'MainProductList',
  components: {
    CardProduct
  },
  // data () {
  // },
  props: {
  },
  setup () {
    const goodsStore = useGoodsStore()
    const basketStore = useBasketStore()

    // Создаем вычисляемое свойство для получения списка товаров
    const prodCardData = computed(() => goodsStore.getGoods)

    // Создаем функцию для добавления товара в корзину
    const addToBasket = (goodId) => {
      basketStore.addGoodInBasket(goodId)
    }
    
    return {
      prodCardData,
      addToBasket
    }
  }
}
</script>

<style lang="scss" scoped>
.main {
  padding-top: 170px;
  display: grid;
  grid-template-columns: repeat(4, 312px);
  justify-content: center;
  grid-column-gap: 20px;
  grid-row-gap: 35px;
}
</style>
