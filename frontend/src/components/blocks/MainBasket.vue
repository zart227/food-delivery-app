<template>
  <div class="main">
    <CardProduct
      v-for="( cartData, index ) in prodCartData"
      :key="index"
      :product-id="cartData.id"
      :title="cartData.title"
      :description="cartData.description"
      :price="cartData.price"
      :image-source="cartData.imageSource"
      :line="true"
      @click-basket="removeFromBasket(index)"
    />
  </div>
</template>

<script>
// import { ref } from 'vue'
import { computed } from 'vue'
import CardProduct from '../elements/CardProduct.vue'
import { useBasketStore } from '@/stores/basket'
export default {
  name: 'MainBasket',
  components: {
    CardProduct
  },
  props: {
  },
  // data () {
  // },
  setup () {
    const basketStore = useBasketStore()

    const prodCartData = computed(() => basketStore.getBasketGoods)

    // Создаем функцию для удаления товара из корзины
    const removeFromBasket = (goodIndex) => {
      basketStore.removeGoodFromBasket(goodIndex)
    }
    return {
      prodCartData,
      removeFromBasket
    }
  }
}
</script>

<style lang="scss" scoped>
.main {
  display: flex;
  flex-direction: column;
  gap: 35px;
}
</style>
