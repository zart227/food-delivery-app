<template>
  <div class="main">
    <div v-for="cartItem in prodCartData" :key="cartItem.id" class="cart-item">
      <CardProduct
        :product-id="cartItem.product_data.id"
        :title="cartItem.product_data.title"
        :description="cartItem.product_data.description"
        :price="cartItem.product_data.price"
        :quantity="cartItem.quantity"
        :line="true"
        :image-source="cartItem.product_data.image"
        @click-basket="removeFromBasket(cartItem.id)"
        @update-quantity="updateQuantity(cartItem.id, $event)"
      />
      <!-- <div class="quantity-controls">
        <button @click="decreaseQuantity(cartItem.id, cartItem.quantity)">
          -
        </button>
        <input
          v-model.number="cartItem.quantity"
          type="number"
          @change="updateQuantity(cartItem.id, cartItem.quantity)"
        />
        <button @click="increaseQuantity(cartItem.id, cartItem.quantity)">
          +
        </button>
      </div> -->
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import CardProduct from '../elements/CardProduct.vue'
import { useBasketStore } from '@/stores/basket'
import { useToast } from 'vue-toastification'

export default {
  name: 'MainBasket',
  components: {
    CardProduct,
  },
  setup() {
    const basketStore = useBasketStore()
    const toast = useToast()
    const prodCartData = computed(() => basketStore.getBasketGoods)

    const removeFromBasket = async (basketItemId) => {
      try {
        await basketStore.removeGoodFromBasket(basketItemId)
      } catch (error) {
        toast.error('Ошибка удаления товара из корзины!')
        console.error('Ошибка удаления товара из корзины:', error)
      }
    }

    const updateQuantity = async (basketItemId, quantity) => {
      if (quantity < 1) return
      try {
        await basketStore.updateBasketItemQuantity(basketItemId, quantity)
      } catch (error) {
        toast.error('Ошибка обновления количества товара!')
        console.error('Ошибка обновления количества товара:', error)
      }
    }

    const increaseQuantity = (basketItemId, currentQuantity) => {
      updateQuantity(basketItemId, currentQuantity + 1)
    }

    const decreaseQuantity = (basketItemId, currentQuantity) => {
      if (currentQuantity > 1) {
        updateQuantity(basketItemId, currentQuantity - 1)
      }
    }

    return {
      prodCartData,
      removeFromBasket,
      updateQuantity,
      increaseQuantity,
      decreaseQuantity,
      toast,
    }
  },
}
</script>

<style lang="scss" scoped>
.main {
  display: flex;
  flex-direction: column;
  gap: 35px;
}

.cart-item {
  // display: flex;
  // justify-content: space-between;
  // align-items: center;
  margin-bottom: 20px;
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
