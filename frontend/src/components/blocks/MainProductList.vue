<template>
  <div class="main">
    <CardProduct
      v-for="cardData in products"
      :key="cardData.id"
      :product-id=cardData.id
      :title="cardData.title"
      :description="cardData.description"
      :price="cardData.price"
      :image-source="cardData.image"
      @click-main = "handleAddToBasket(cardData.id)"
    />
  </div>
</template>

<script>
import { onMounted, computed } from 'vue'
import CardProduct from '../elements/CardProduct.vue'
import { useBasketStore } from '@/stores/basket'
import { useProductsStore } from '@/stores/products'
import { useToast } from 'vue-toastification'

export default {
  name: 'MainProductList',
  components: {
    CardProduct,
  },
  setup() {
    const basketStore = useBasketStore()
    const productsStore = useProductsStore()
    const toast = useToast()

    // Загружаем список товаров при монтировании
    onMounted(async () => {
      try {
        await productsStore.fetchAllProducts()
      } catch (error) {
        toast.error('Ошибка загрузки товаров!')
        console.error('Ошибка загрузки товаров:', error)
      }
    })

    // Получаем список товаров из стора
    const products = computed(() => productsStore.getProductList)

    // Добавление товара в корзину
    const handleAddToBasket = (productId) => {
      toast.success('Товар добавлен в корзину!')
      basketStore.addGoodInBasket(productId)
    }

    // Форматирование цены
    // const formatPrice = (price) => {
    //   const numericPrice = parseFloat(price)
    //   return isNaN(numericPrice) ? '0.00' : numericPrice.toFixed(2)
    // }

    return {
      products,
      handleAddToBasket,
      // formatPrice,
      toast
    }
  },
}
</script>

<style lang="scss" scoped>
.main {
  padding-top: 20px;
  display: grid;
  grid-template-columns: repeat(4, 312px);
  justify-content: center;
  grid-column-gap: 20px;
  grid-row-gap: 35px;
}
</style>
